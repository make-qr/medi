---
layout: default
title: Gentle Habits
permalink: /category/gentle-habits/
full_width: true
page_kind: archive
excerpt: Walking, talking, stress, and small daily habits that support connection.
category_slug: gentle-habits
---

<section class="archive-header">
  <h1>Gentle Habits</h1>
  <p class="archive-lead">Small, sustainable habits — walking with a voice, easing stress, and ordinary routines that keep you linked to other people.</p>
</section>

{% include category-pills.html active='gentle-habits' %}

<section class="home-section archive-listing">
  <div class="post-card-grid">
    {% for post in site.posts %}
      {% if post.category_slug == 'gentle-habits' %}
        {% include post-card.html post=post %}
      {% endif %}
    {% endfor %}
  </div>
</section>
