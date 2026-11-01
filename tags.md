---
layout: default
title: Browse by tag
nosidebar: true
---
<div class="tagspage" style="background-color:#000; color:#fff;">
  <h1 style="color:#fff;">Browse by tag</h1>
  <p style="color:#ccc;"><a href="{{ '/' | relative_url }}">&larr; back to the journal</a> &mdash; every tag used on a journal page, with its pages newest first.</p>
  {% comment %}Collect all tags from all posts. Liquid can't concat arrays natively in
  older versions, so use a string of '|tag|' markers and split it back out.{% endcomment %}
  {% assign tagstr = "" %}
  {% for post in site.posts %}
    {% for tag in post.tags %}
      {% assign tagstr = tagstr | append: "|" | append: tag | append: "|" %}
    {% endfor %}
  {% endfor %}
  {% assign alltags = tagstr | split: "|" | uniq | sort %}
  <p style="color:#888; font-size:small;">{{ alltags.size }} tags</p>
  {% for tag in alltags %}
    <h2 id="{{ tag | slugify }}">{{ tag }} <span class="tagcount">({% assign n = 0 %}{% for post in site.posts %}{% if post.tags contains tag %}{% assign n = n | plus: 1 %}{% endif %}{% endfor %}{{ n }})</span></h2>
    <ul>
    {% assign posts = site.posts | sort: "date" | reverse %}
    {% for post in posts %}
      {% if post.tags contains tag %}
      <li><a href="{{ post.url | relative_url }}">{{ post.title }}</a></li>
      {% endif %}
    {% endfor %}
    </ul>
  {% endfor %}
  <hr style="border-color:#333;"/>
  <p style="color:#888; font-size:small;">&copy; {{ site.time | date: "%Y" }} by AtaraxiA under Creative Commons BY-SA</p>
</div>
