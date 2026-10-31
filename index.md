---
layout: default
title: Index
---
<div class="index" style="background-color:#000; color:#fff;">
  <h1 style="color:#fff;">RubberNaut — The Thalia Journal</h1>
  <p style="color:#ccc;">An epistolary journal, in chronological order. Newest entries first.</p>
  <p style="color:#888; font-size:small;">&copy; 2026 by AtaraxiA under Creative Commons BY-SA</p>
  <hr style="border-color:#333;"/>
  <ul>
  {% assign posts = site.posts | sort: "date" | reverse %}
  {% for post in posts %}
    <li>
      <a href="{{ post.url | relative_url }}">{{ post.title }}</a>
      <span style="color:#888; font-size:small;"> — {{ post.date | date: "%Y-%m-%d %H:%M" }}</span>
    </li>
  {% endfor %}
  </ul>
</div>
