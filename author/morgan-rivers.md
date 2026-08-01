---
layout: default
title: Morgan Rivers
permalink: /author/morgan-rivers/
full_width: true
page_kind: archive
excerpt: Staff Essayist at OmegleChat Medi — loneliness, sleep, gentle habits, and the courage to stay connected.
---

<section class="archive-header">
  <h1>Morgan Rivers</h1>
  <p class="archive-lead">Staff Essayist · OmegleChat Medi — loneliness, sleep, gentle habits, and staying connected without medical jargon.</p>
</section>

{% include category-pills.html active='all' %}

<section class="home-section">
  <div class="author-card">
    <p>Morgan Rivers writes <strong>long-form</strong> health-light essays for people who feel disconnected — not clinical manuals. Pieces are research-informed, warm, and always end with a reminder that they are not medical advice.</p>
    <p style="margin-bottom:0">Also writing on <a href="{{ site.blog_site }}">OmegleChat Blog</a> (stories, Love Journey, Later Years).</p>
  </div>
</section>

<section class="home-section">
  <h2 class="section-title">Latest by Morgan Rivers</h2>
  <div class="post-card-grid">
    {% for post in site.posts %}
      {% if post.author_slug == 'morgan-rivers' or post.author == 'Morgan Rivers' %}
        {% include post-card.html post=post %}
      {% endif %}
    {% endfor %}
  </div>
</section>
