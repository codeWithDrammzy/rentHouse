{% extends "soniHouseAgent/adminpage/base.html" %}

{% block content %}
<main class="col-span-1 md:col-span-8 px-4">
  <div class="max-w-7xl mx-auto space-y-8 mt-4">

    <!-- Header with Title and Add Button -->
    <div class="flex justify-between items-center border-b pb-2">
      <h2 class="text-2xl font-bold text-blue-800">Property Listings</h2>
      <a href="" class="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 transition">
        <svg xmlns="http://www.w3.org/2000/svg" class="w-5 h-5 mr-2" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 4v16m8-8H4"/>
        </svg>
        Add New
      </a>
    </div>

    <!-- Table of Properties -->
    <div class="overflow-x-auto bg-white rounded-lg shadow">
      <table class="min-w-full table-auto">
        <thead class="bg-gray-100 text-left text-gray-700 uppercase text-sm font-semibold">
  <tr>
    <th class="px-6 py-3">Title</th>
    <th class="px-6 py-3">Location</th>
    <th class="px-6 py-3">Price</th>
    <th class="px-6 py-3">Bedrooms</th>
    <th class="px-6 py-3">Bathrooms</th>
    <th class="px-6 py-3">Owner</th>  <!-- ✅ New Column -->
    <th class="px-6 py-3">Status</th>
    <th class="px-6 py-3">Actions</th>
  </tr>
</thead>
<tbody class="text-sm text-gray-800">
  {% for property in properties %}
  <tr class="border-b hover:bg-gray-50">
    <td class="px-6 py-3">{{ property.title }}</td>
    <td class="px-6 py-3">{{ property.location }}</td>
    <td class="px-6 py-3">₦{{ property.price|floatformat:2 }}</td>
    <td class="px-6 py-3">{{ property.num_bedrooms }}</td>
    <td class="px-6 py-3">{{ property.num_bathrooms }}</td>
    <td class="px-6 py-3">{{ property.owner.first_name }} {{ property.owner.last_name }}</td>  <!-- ✅ Owner info -->
    <td class="px-6 py-3">
      {% if property.is_available %}
        <span class="text-green-600 font-semibold">Available</span>
      {% else %}
        <span class="text-red-500 font-semibold">Occupied</span>
      {% endif %}
    </td>
    <td class="px-6 py-3 space-x-2">
      <a href="{% url 'view_property' property.id %}" class="text-blue-600 hover:underline">View</a>
      <a href="{% url 'edit_property' property.id %}" class="text-yellow-600 hover:underline">Edit</a>
      <a href="{% url 'delete_property' property.id %}" class="text-red-600 hover:underline">Delete</a>
    </td>
  </tr>
  {% endfor %}
</tbody>

      </table>
    </div>

  </div>
</main>
{% endblock %}
