---
layout: default
title: Connection Health
permalink: /category/connection-health/
full_width: true
page_kind: archive
excerpt: Loneliness, isolation, and the quiet work of staying connected — essays for ordinary lonely hours.
category_slug: connection-health
---

<section class="archive-header">
  <h1>Connection Health</h1>
  <p class="archive-lead">Loneliness, isolation, and reaching out — written for real nights, not textbooks.</p>
</section>

{% include category-pills.html active='connection-health' %}

<section class="home-section archive-listing">
  <div class="post-card-grid">
    {% for post in site.posts %}
      {% if post.category_slug == 'connection-health' %}
        {% include post-card.html post=post %}
      {% endif %}
    {% endfor %}
  </div>
</section>
