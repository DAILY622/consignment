#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Fix home.html template"""

content = """{% extends 'base.html' %}
{% load static %}

{% block title %}DailyFX Delivery - Cybernetic Parcel Delivery & Tracking{% endblock %}

{% block extra_head %}
<style>
    /* GlitchD Cyberpunk Theme */
    :root {
        --neon-cyan: #00f0ff;
        --neon-magenta: #ff00ff;
        --neon-purple: #b030ff;
        --neon-green: #39ff14;
        --dark-bg: #0a0a0f;
        --dark-card: #111118;
        --dark-accent: #1a1a2e;
    }
    
    body { background: #0a0a0f !important; color: #00f0ff !important; }
    
    .glitch { position: relative; font-weight: 900; text-transform: uppercase; }
    .neon-glow { text-shadow: 0 0 10px var(--neon-cyan), 0 0 20px var(--neon-cyan), 0 0 30px var(--neon-cyan); }
    .neon-border { box-shadow: 0 0 10px var(--neon-purple), 0 0 20px var(--neon-purple); border: 2px solid var(--neon-purple); }
    
    .matrix-bg { position: relative; overflow: hidden; background: linear-gradient(135deg, #0a0a0f 0%, #1a1a2e 50%, #0a0a0f 100%); }
    
    .cyber-card {
        background: linear-gradient(135deg, rgba(17, 17, 24, 0.95), rgba(26, 26, 46, 0.9));
        border: 2px solid var(--neon-purple);
        transition: all 0.3s;
    }
    .cyber-card:hover { transform: translateY(-5px); box-shadow: 0 0 30px rgba(0, 240, 255, 0.5); }
    
    .scan-line {
        position: fixed; top: 0; left: 0; width: 100%; height: 2px;
        background: linear-gradient(90deg, transparent, var(--neon-cyan), transparent);
        animation: scan 8s linear infinite;
        pointer-events: none; z-index: 9999; opacity: 0.3;
    }
    @keyframes scan { 0% { transform: translateY(-100%); } 100% { transform: translateY(100vh); } }
    
    .cyber-button {
        background: linear-gradient(135deg, var(--neon-cyan), var(--neon-purple));
        border: none; transition: all 0.3s;
    }
    .cyber-button:hover {
        box-shadow: 0 0 20px var(--neon-cyan), 0 0 40px var(--neon-purple);
        transform: scale(1.05);
    }
    
    .grid-bg {
        background-image: 
            linear-gradient(rgba(0, 240, 255, 0.1) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 240, 255, 0.1) 1px, transparent 1px);
        background-size: 50px 50px;
        animation: grid-move 20s linear infinite;
    }
    @keyframes grid-move { 0% { background-position: 0 0; } 100% { background-position: 50px 50px; } }
    
    .hologram { background: linear-gradient(180deg, rgba(0, 240, 255, 0.1) 0%, transparent 100%); position: relative; }
</style>
{% endblock %}

{% block content %}
<!-- Scan Line Effect -->
<div class="scan-line"></div>

<!-- Hero Section -->
<div class="matrix-bg rounded-2xl p-12 mb-12 relative overflow-hidden min-h-[600px] flex items-center neon-border">
    <div class="grid-bg absolute inset-0 opacity-30"></div>
    <div class="grid md:grid-cols-2 gap-8 items-center relative z-10 w-full">
        <div>
            <span class="bg-gradient-to-r from-cyan-500 to-purple-500 text-black text-sm px-4 py-2 rounded-full mb-4 inline-flex items-center gap-2 font-bold">
                <span class="w-2 h-2 bg-green-400 rounded-full animate-pulse"></span>
                #1 CYBER DELIVERY NETWORK
            </span>
            <h1 class="text-5xl font-bold mb-4 leading-tight neon-glow glitch" data-text="DAILYFX CYBER LOGISTICS">
                DAILYFX CYBER LOGISTICS
            </h1>
            <p class="text-xl text-cyan-300 mb-4 leading-relaxed">
                Next-generation delivery powered by quantum tracking, neural networks, and blockchain verification.
            </p>
            <p class="text-lg text-purple-300 mb-8">
                Same-day drone delivery • Neural GPS tracking • Quantum-secured routes • 24/7 AI support
            </p>
            <div class="flex flex-wrap gap-4">
                <a href="{% url 'track' %}" class="cyber-button text-black px-8 py-3 rounded-lg font-bold shadow-lg flex items-center gap-2">
                    <svg class="w-5 h-5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M17.657 16.657L13.414 20.9a1.998 1.998 0 01-2.827 0l-4.244-4.243a8 8 0 1111.314 0z"/><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 11a3 3 0 11-6 0 3 3 0 016 0z"/></svg>
                    TRACK PACKAGE
                </a>
                {% if not user.is_authenticated %}
                    <a href="{% url 'register' %}" class="border-2 border-cyan-400 text-cyan-400 px-8 py-3 rounded-lg font-bold hover:bg-cyan-400 hover:text-black transition neon-border">JACK IN</a>
                {% else %}
                    <a href="{% url 'create_package' %}" class="border-2 border-magenta-400 text-magenta-400 px-8 py-3 rounded-lg font-bold hover:bg-magenta-400 hover:text-black transition">+ SEND DATA</a>
                {% endif %}
                <a href="#quote" class="bg-gradient-to-r from-purple-600 to-pink-600 text-white px-8 py-3 rounded-lg font-bold transition">
                    💳 REQUEST QUOTE
                </a>
            </div>
            <div class="flex items-center gap-6 mt-8 pt-6 border-t border-cyan-500/30">
                <div class="flex -space-x-3">
                    <img src="{% static 'images/team-ceo.jpg' %}" class="w-10 h-10 rounded-full border-2 border-cyan-400 object-cover hologram" alt="Customer">
                    <img src="{% static 'images/team-fleet.jpg' %}" class="w-10 h-10 rounded-full border-2 border-purple-400 object-cover hologram" alt="Customer">
                    <img src="{% static 'images/team-operations.jpg' %}" class="w-10 h-10 rounded-full border-2 border-magenta-400 object-cover hologram" alt="Customer">
                </div>
                <div>
                    <div class="flex text-green-400 text-sm neon-glow">★★★★★</div>
                    <p class="text-sm text-cyan-200">50,000+ netrunners trust us</p>
                </div>
            </div>
        </div>
        <div class="hidden md:block hologram">
            <img src="{% static 'images/hero-delivery.jpg' %}" alt="Cyber Delivery" class="rounded-2xl shadow-2xl border-2 border-cyan-400 transform hover:scale-105 transition-transform duration-500">
        </div>
    </div>
</div>

<!-- Quick Track -->
<div class="cyber-card rounded-xl p-8 mb-12">
    <h2 class="text-2xl font-bold text-cyan-400 mb-4 neon-glow">QUANTUM TRACK</h2>
    <form action="{% url 'track' %}" method="GET" class="flex flex-col md:flex-row gap-4">
        <input type="text" name="q" placeholder="Enter tracking number (e.g., DFX-XXXXXXXX)" 
               class="flex-1 px-4 py-3 border-2 border-purple-500 rounded-lg bg-black text-cyan-300 focus:border-cyan-400 focus:outline-none">
        <button type="submit" class="cyber-button px-8 py-3 rounded-lg font-bold text-black">
            TRACK NOW
        </button>
    </form>
</div>

<!-- Services & Pricing -->
<div class="mb-16" id="services">
    <div class="text-center mb-10">
        <h2 class="text-3xl font-bold text-cyan-400 mb-2 neon-glow">CYBER SERVICES</h2>
        <p class="text-purple-300">Choose your delivery protocol</p>
    </div>
    <div class="grid md:grid-cols-3 gap-8">
        <div class="cyber-card rounded-xl p-6">
            <div class="text-center mb-6">
                <h3 class="text-2xl font-bold text-cyan-400 mb-2">STANDARD</h3>
                <p class="text-purple-300 mb-4">2-3 Business Days</p>
                <span class="text-4xl font-bold text-cyan-400 neon-glow">£{{ site_settings.price_standard }}</span>
                <span class="text-purple-400">/parcel</span>
            </div>
            <ul class="space-y-3 mb-6 text-cyan-300">
                <li class="flex items-center"><span class="text-green-400 mr-2 neon-glow">✓</span> Up to 20kg</li>
                <li class="flex items-center"><span class="text-green-400 mr-2 neon-glow">✓</span> GPS Tracking</li>
                <li class="flex items-center"><span class="text-green-400 mr-2 neon-glow">✓</span> Email Updates</li>
                <li class="flex items-center"><span class="text-green-400 mr-2 neon-glow">✓</span> £{{ site_settings.coverage_standard|floatformat:0 }} Cover</li>
            </ul>
            <a href="{% url 'register' %}" class="block text-center cyber-button py-3 rounded-lg font-bold text-black">SELECT STANDARD</a>
        </div>
        
        <div class="cyber-card rounded-xl p-6 transform scale-105 neon-border">
            <div class="text-center mb-6">
                <span class="bg-yellow-400 text-black text-xs px-2 py-1 rounded-full font-bold mb-2 inline-block">POPULAR</span>
                <h3 class="text-2xl font-bold text-cyan-400 mb-2">EXPRESS</h3>
                <p class="text-purple-300 mb-4">Next Business Day</p>
                <span class="text-4xl font-bold text-cyan-400 neon-glow">£{{ site_settings.price_next_day }}</span>
                <span class="text-purple-400">/parcel</span>
            </div>
            <ul class="space-y-3 mb-6 text-cyan-300">
                <li class="flex items-center"><span class="text-green-400 mr-2 neon-glow">✓</span> Up to 30kg</li>
                <li class="flex items-center"><span class="text-green-400 mr-2 neon-glow">✓</span> Live GPS Tracking</li>
                <li class="flex items-center"><span class="text-green-400 mr-2 neon-glow">✓</span> SMS + Email Updates</li>
                <li class="flex items-center"><span class="text-green-400 mr-2 neon-glow">✓</span> £{{ site_settings.coverage_next_day|floatformat:0 }} Cover</li>
                <li class="flex items-center"><span class="text-green-400 mr-2 neon-glow">✓</span> Priority Handling</li>
            </ul>
            <a href="{% url 'register' %}" class="block text-center bg-gradient-to-r from-cyan-500 to-purple-500 text-black py-3 rounded-lg font-bold hover:scale-105 transition">SELECT EXPRESS</a>
        </div>
        
        <div class="cyber-card rounded-xl p-6">
            <div class="text-center mb-6">
                <h3 class="text-2xl font-bold text-pink-400 mb-2">SAME DAY</h3>
                <p class="text-purple-300 mb-4">Delivered Today</p>
                <span class="text-4xl font-bold text-pink-400 neon-glow">£{{ site_settings.price_same_day }}</span>
                <span class="text-purple-400">/parcel</span>
            </div>
            <ul class="space-y-3 mb-6 text-cyan-300">
                <li class="flex items-center"><span class="text-green-400 mr-2 neon-glow">✓</span> Up to 30kg</li>
                <li class="flex items-center"><span class="text-green-400 mr-2 neon-glow">✓</span> Real-Time Tracking</li>
                <li class="flex items-center"><span class="text-green-400 mr-2 neon-glow">✓</span> Instant Notifications</li>
                <li class="flex items-center"><span class="text-green-400 mr-2 neon-glow">✓</span> £200 Cover</li>
                <li class="flex items-center"><span class="text-green-400 mr-2 neon-glow">✓</span> Dedicated Courier</li>
            </ul>
            <a href="{% url 'register' %}" class="block text-center bg-gradient-to-r from-pink-500 to-red-500 text-black py-3 rounded-lg font-bold hover:scale-105 transition">SELECT SAME DAY</a>
        </div>
    </div>
</div>

<!-- Stats -->
<div class="matrix-bg rounded-xl p-8 mb-16 neon-border">
    <div class="grid-bg absolute inset-0 opacity-20"></div>
    <div class="grid md:grid-cols-4 gap-8 text-center relative z-10">
        <div>
            <div class="text-4xl font-bold text-cyan-400 neon-glow">50K+</div>
            <div class="text-purple-300">Packages Delivered</div>
        </div>
        <div>
            <div class="text-4xl font-bold text-green-400 neon-glow">99.2%</div>
            <div class="text-purple-300">On-Time Delivery</div>
        </div>
        <div>
            <div class="text-4xl font-bold text-purple-400 neon-glow">500+</div>
            <div class="text-purple-300">Active Drivers</div>
        </div>
        <div>
            <div class="text-4xl font-bold text-yellow-400 neon-glow">24/7</div>
            <div class="text-purple-300">AI Support</div>
        </div>
    </div>
</div>

<!-- Quote Calculator -->
<div class="cyber-card rounded-2xl p-8 mb-16 neon-border" id="quote">
    <div class="max-w-4xl mx-auto">
        <div class="text-center mb-8">
            <h2 class="text-3xl font-bold text-cyan-400 mb-2 neon-glow">💳 INSTANT QUOTE</h2>
            <p class="text-purple-300">Calculate your shipping cost in nanoseconds</p>
        </div>
        <div class="cyber-card rounded-xl p-6">
            <div class="grid md:grid-cols-4 gap-4 mb-6">
                <div>
                    <label class="block text-sm font-medium text-cyan-400 mb-1">FROM</label>
                    <input type="text" id="quote-from" placeholder="e.g., SW1A 1AA" 
                           class="w-full px-4 py-3 border-2 border-purple-500 rounded-lg bg-black text-cyan-300 focus:border-cyan-400 focus:outline-none">
                </div>
                <div>
                    <label class="block text-sm font-medium text-cyan-400 mb-1">TO</label>
                    <input type="text" id="quote-to" placeholder="e.g., M1 1AD" 
                           class="w-full px-4 py-3 border-2 border-purple-500 rounded-lg bg-black text-cyan-300 focus:border-cyan-400 focus:outline-none">
                </div>
                <div>
                    <label class="block text-sm font-medium text-cyan-400 mb-1">WEIGHT (kg)</label>
                    <input type="number" id="quote-weight" placeholder="5" min="0.1" step="0.1"
                           class="w-full px-4 py-3 border-2 border-purple-500 rounded-lg bg-black text-cyan-300 focus:border-cyan-400 focus:outline-none">
                </div>
                <div>
                    <label class="block text-sm font-medium text-cyan-400 mb-1">SERVICE</label>
                    <select id="quote-service" class="w-full px-4 py-3 border-2 border-purple-500 rounded-lg bg-black text-cyan-300 focus:border-cyan-400 focus:outline-none">
                        <option value="standard">Standard (2-3 days)</option>
                        <option value="express" selected>Express (Next day)</option>
                        <option value="sameday">Same Day</option>
                    </select>
                </div>
            </div>
            <div class="flex flex-col md:flex-row items-center justify-between gap-4">
                <button onclick="calculateQuote()" class="w-full md:w-auto cyber-button text-black px-8 py-3 rounded-lg font-bold">
                    CALCULATE PRICE
                </button>
                <div id="quote-result" class="text-center md:text-right">
                    <p class="text-sm text-purple-400">Estimated Price</p>
                    <p class="text-3xl font-bold text-cyan-400 neon-glow">£--</p>
                </div>
            </div>
        </div>
    </div>
</div>

<!-- Newsletter -->
<div class="cyber-card rounded-2xl p-8 mb-16 text-center neon-border">
    <h2 class="text-3xl font-bold text-cyan-400 mb-4 neon-glow">STAY CONNECTED</h2>
    <p class="text-purple-300 mb-6">Subscribe to our neural network for cyber updates and quantum insights.</p>
    <form action="{% url 'home' %}" method="POST" class="max-w-md mx-auto">
        {% csrf_token %}
        <div class="flex gap-4">
            <input type="email" name="newsletter_email" placeholder="Enter your email" required
                   class="flex-1 px-4 py-3 border-2 border-purple-500 rounded-lg bg-black text-cyan-300 focus:border-cyan-400 focus:outline-none">
            <button type="submit" class="cyber-button text-black px-8 py-3 rounded-lg font-bold">
                SUBSCRIBE
            </button>
        </div>
    </form>
</div>

<script>
function calculateQuote() {
    const weight = parseFloat(document.getElementById('quote-weight').value) || 0;
    const service = document.getElementById('quote-service').value;
    
    let basePrice = 0;
    if (service === 'standard') basePrice = {{ site_settings.price_standard }};
    if (service === 'express') basePrice = {{ site_settings.price_next_day }};
    if (service === 'sameday') basePrice = {{ site_settings.price_same_day }};
    
    let weightSurcharge = 0;
    if (weight > 0 && weight <= 1) weightSurcharge = {{ site_settings.price_weight_1kg }};
    else if (weight > 1 && weight <= 5) weightSurcharge = {{ site_settings.price_weight_5kg }};
    else if (weight > 5 && weight <= 10) weightSurcharge = {{ site_settings.price_weight_10kg }};
    else if (weight > 10 && weight <= 20) weightSurcharge = {{ site_settings.price_weight_20kg }};
    else if (weight > 20 && weight <= 30) weightSurcharge = {{ site_settings.price_weight_30kg }};
    else if (weight > 30) weightSurcharge = {{ site_settings.price_weight_50kg }};
    
    const total = (parseFloat(basePrice) + parseFloat(weightSurcharge)).toFixed(2);
    document.getElementById('quote-result').querySelector('p:last-child').innerHTML = `<span class="neon-glow">£${total}</span>`;
}
</script>

{% endblock %}
"""

with open('templates/home.html', 'w', encoding='utf-8') as f:
    f.write(content)

print("✅ home.html created successfully!")
