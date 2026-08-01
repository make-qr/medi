---
layout: default
title: Lived Stories
permalink: /category/lived-stories/
full_width: true
page_kind: archive
excerpt: First-person essays on caregiving, quiet parents, and living with hard days.
category_slug: lived-stories
---

<section class="archive-header">
  <h1>Lived Stories</h1>
  <p class="archive-lead">First-person essays — caregiving, quiet parents, and the days that don’t fit a neat health tip.</p>
</section>

{% include category-pills.html active='lived-stories' %}

<section class="home-section archive-listing">
  <div class="post-card-grid">
    {% for post in site.posts %}
      {% if post.category_slug == 'lived-stories' %}
        {% include post-card.html post=post %}
      {% endif %}
    {% endfor %}
  </div>
  {% assign ls = site.posts | where: "category_slug", "lived-stories" | size %}
  {% if ls == 0 %}
  <p class="text-muted">Lived stories publishing soon. Start with <a href="{{ '/loneliness-vs-solitude/' | relative_url }}">loneliness vs solitude</a>.</p>
  {% endif %}
</section>
