---
layout: default
title: Brain & Aging
permalink: /category/brain-aging/
full_width: true
page_kind: archive
excerpt: Conversation, cognition, and staying socially engaged as we age.
category_slug: brain-aging
---

<section class="archive-header">
  <h1>Brain &amp; Aging</h1>
  <p class="archive-lead">What research suggests about conversation, isolation, and keeping the mind engaged later in life.</p>
</section>

{% include category-pills.html active='brain-aging' %}

<section class="home-section archive-listing">
  <div class="post-card-grid">
    {% for post in site.posts %}
      {% if post.category_slug == 'brain-aging' %}
        {% include post-card.html post=post %}
      {% endif %}
    {% endfor %}
  </div>
</section>
