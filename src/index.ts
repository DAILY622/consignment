// Full Cloudflare Stack - TypeScript Worker Entry Point
// R2 + D1 + Queues + Durable Objects

export interface Env {
	// D1 Database
	DB: D1Database;
	
	// R2 Storage
	MEDIA: R2Bucket;
	
	// Queue for async tasks
	DELIVERY_QUEUE: Queue;
	
	// Durable Objects
	PACKAGE_TRACKER: DurableObjectNamespace;
	DELIVERY_ROOM: DurableObjectNamespace;
	
	// KV Cache
	CACHE: KVNamespace;
}

// ===== MAIN WORKER =====
export default {
	async fetch(request: Request, env: Env, ctx: ExecutionContext): Promise<Response> {
		const url = new URL(request.url);
		
		// Route: Track package
		if (url.pathname.startsWith('/api/track/')) {
			const trackingNumber = url.pathname.split('/').pop()!;
			return await trackPackage(trackingNumber, env);
		}
		
		// Route: Upload delivery photo
		if (url.pathname === '/api/upload' && request.method === 'POST') {
			return await uploadPhoto(request, env);
		}
		
		// Route: Real-time tracking WebSocket
		if (url.pathname === '/ws/track' && request.headers.get('Upgrade') === 'websocket') {
			return await handleWebSocket(request, env);
		}
		
		return new Response('Consignment Delivery API', { status: 200 });
	},
	
	// Queue Consumer - Process delivery notifications
	async queue(batch: MessageBatch<any>, env: Env): Promise<void> {
		for (const message of batch.messages) {
			await processDeliveryNotification(message.body, env);
		}
	}
};

// ===== TRACK PACKAGE =====
async function trackPackage(trackingNumber: string, env: Env): Promise<Response> {
	// Check cache first
	const cached = await env.CACHE.get(`track:${trackingNumber}`);
	if (cached) {
		return new Response(cached, {
			headers: { 'Content-Type': 'application/json' }
		});
	}
	
	// Query D1 database
	const result = await env.DB.prepare(
		'SELECT * FROM packages_package WHERE tracking_number = ?'
	).bind(trackingNumber).first();
	
	if (!result) {
		return new Response(JSON.stringify({ error: 'Package not found' }), {
			status: 404,
			headers: { 'Content-Type': 'application/json' }
		});
	}
	
	// Get tracking history
	const history = await env.DB.prepare(
		'SELECT * FROM tracking_trackinghistory WHERE package_id = ? ORDER BY timestamp DESC'
	).bind(result.id).all();
	
	const response = {
		package: result,
		history: history.results
	};
	
	// Cache for 5 minutes
	await env.CACHE.put(`track:${trackingNumber}`, JSON.stringify(response), {
		expirationTtl: 300
	});
	
	return new Response(JSON.stringify(response), {
		headers: { 'Content-Type': 'application/json' }
	});
}

// ===== UPLOAD PHOTO TO R2 =====
async function uploadPhoto(request: Request, env: Env): Promise<Response> {
	const formData = await request.formData();
	const file = formData.get('photo');
	const trackingNumber = formData.get('tracking_number') as string;
	
	if (!file || typeof file === 'string') {
		return new Response('No file uploaded', { status: 400 });
	}
	
	// file is now typed as File
	const uploadedFile = file as File;
	
	// Generate unique filename
	const filename = `delivery_photos/${trackingNumber}_${Date.now()}.${uploadedFile.name.split('.').pop()}`;
	
	// Upload to R2
	await env.MEDIA.put(filename, uploadedFile.stream(), {
		httpMetadata: {
			contentType: uploadedFile.type
		}
	});
	
	// Update database
	await env.DB.prepare(
		'UPDATE packages_package SET photo_url = ? WHERE tracking_number = ?'
	).bind(`https://media.yourdomain.com/${filename}`, trackingNumber).run();
	
	// Send notification via Queue
	await env.DELIVERY_QUEUE.send({
		type: 'photo_uploaded',
		tracking_number: trackingNumber,
		photo_url: filename,
		timestamp: new Date().toISOString()
	});
	
	return new Response(JSON.stringify({ success: true, filename }), {
		headers: { 'Content-Type': 'application/json' }
	});
}

// ===== WEBSOCKET FOR REAL-TIME TRACKING =====
async function handleWebSocket(request: Request, env: Env): Promise<Response> {
	const upgradeHeader = request.headers.get('Upgrade');
	if (upgradeHeader !== 'websocket') {
		return new Response('Expected Upgrade: websocket', { status: 426 });
	}
	
	// Get Durable Object ID for this tracking session
	const url = new URL(request.url);
	const trackingNumber = url.searchParams.get('tracking');
	const id = env.DELIVERY_ROOM.idFromName(trackingNumber!);
	const stub = env.DELIVERY_ROOM.get(id);
	
	// Forward to Durable Object
	return stub.fetch(request);
}

// ===== QUEUE CONSUMER =====
async function processDeliveryNotification(message: any, env: Env): Promise<void> {
	console.log('Processing notification:', message);
	
	// Send email notification
	// Send SMS
	// Update real-time tracking
	// Whatever async task needed
	
	// Example: Broadcast to WebSocket clients via Durable Object
	if (message.type === 'status_update') {
		const id = env.PACKAGE_TRACKER.idFromName(message.tracking_number);
		const stub = env.PACKAGE_TRACKER.get(id);
		await stub.fetch(new Request('https://internal/broadcast', {
			method: 'POST',
			body: JSON.stringify(message)
		}));
	}
}

// ===== DURABLE OBJECT: PACKAGE TRACKER =====
export class PackageTracker {
	state: DurableObjectState;
	env: Env;
	
	constructor(state: DurableObjectState, env: Env) {
		this.state = state;
		this.env = env;
	}
	
	async fetch(request: Request): Promise<Response> {
		// Handle real-time updates for specific package
		return new Response('Package tracker');
	}
}

// ===== DURABLE OBJECT: DELIVERY ROOM =====
export class DeliveryRoom {
	state: DurableObjectState;
	sessions: Set<WebSocket>;
	
	constructor(state: DurableObjectState, env: Env) {
		this.state = state;
		this.sessions = new Set();
	}
	
	async fetch(request: Request): Promise<Response> {
		// Accept WebSocket connection
		const pair = new WebSocketPair();
		const [client, server] = Object.values(pair);
		
		this.sessions.add(server);
		
		server.accept();
		server.addEventListener('message', (event) => {
			// Broadcast to all connected clients
			this.broadcast(event.data);
		});
		
		server.addEventListener('close', () => {
			this.sessions.delete(server);
		});
		
		return new Response(null, {
			status: 101,
			webSocket: client
		});
	}
	
	broadcast(message: string): void {
		for (const session of this.sessions) {
			session.send(message);
		}
	}
}
