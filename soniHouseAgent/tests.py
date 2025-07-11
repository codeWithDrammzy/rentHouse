{% extends "soniHouseAgent/adminpage/base.html" %}
{% block content %}
<main class="col-span-1 md:col-span-8 px-4">
  <div class="max-w-4xl mx-auto mt-6 bg-white shadow rounded-lg p-6 space-y-6">

    <!-- Back Button -->
    <a href="#" onclick="history.back()" class="inline-block text-blue-600 hover:underline">
      ← Back to Listings
    </a>

    <!-- Title and Location -->
    <div class="border-b pb-4">
      <h2 class="text-3xl font-bold text-blue-800">Luxury 3-Bedroom Apartment</h2>
      <p class="text-gray-500">Kano City, Nigeria</p>
    </div>

    <!-- Key Details -->
    <div class="grid grid-cols-1 sm:grid-cols-2 gap-4 text-sm text-gray-700">
      <div>
        <span class="font-semibold">Price (Monthly):</span><br>
        ₦150,000.00
      </div>
      <div>
        <span class="font-semibold">Status:</span><br>
        <span class="text-green-600 font-semibold">Available</span>  <!-- Hardcoded status -->
      </div>
      <div>
        <span class="font-semibold">Bedrooms:</span><br>
        3
      </div>
      <div>
        <span class="font-semibold">Bathrooms:</span><br>
        2
      </div>
    </div>

    <!-- Owner Details -->
    <div class="mt-6">
      <h3 class="text-lg font-bold text-gray-800 mb-2">Owner Information</h3>
      <p><span class="font-semibold">Name:</span> Aliyu Dawud</p>
      <p><span class="font-semibold">Phone:</span> 0801 234 5678</p>
    </div>

    <!-- Description -->
    <div class="mt-6">
      <h3 class="text-lg font-bold text-gray-800 mb-2">Description</h3>
      <p class="text-gray-700 leading-relaxed">
        This luxury apartment offers spacious living with 3 bedrooms and 2 modern bathrooms. 
        Located in the heart of Kano City, it features excellent lighting, tiled floors, and a 
        quiet environment. Perfect for families or professionals looking for comfort and convenience.
      </p>
    </div>

  </div>
</main>
{% endblock %}
