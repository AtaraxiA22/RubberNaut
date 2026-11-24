---
layout: default
title: "Table of Contents"
permalink: /toc.html
---
<p class="lastread" hidden><a id="lastread-link" href="#">[Open My last Read]</a></p>
<div class="toctable">
<table class="toc" id="toctable">
<thead>
<tr>
  <th class="col-story">StoryDate:
    <button type="button" class="sortbtn" data-sort="story-desc" title="newest first">&darr;</button>
    <button type="button" class="sortbtn" data-sort="story-asc" title="oldest first">&uarr;</button>
  </th>
  <th class="col-pub">PostDate:
    <button type="button" class="sortbtn" data-sort="pub-desc" title="newest first">&darr;</button>
    <button type="button" class="sortbtn" data-sort="pub-asc" title="oldest first">&uarr;</button>
  </th>
  <th class="col-title">Title</th>
</tr>
</thead>
<tbody id="tocbody">
{% assign posts = site.journal | sort: "storydate" %}
{% for post in posts %}
<tr data-story="{{ post.storydate }}" data-pub="{{ post.postdate }}">
  <td class="col-story">{{ post.storydate }}</td>
  <td class="col-pub">{{ post.postdate }}</td>
  <td class="col-title"><a href="{{ post.url | relative_url }}">{{ post.storydate }} - {{ post.title }}</a></td>
</tr>
{% endfor %}
</tbody>
</table>
</div>
<script>
(function () {
  var tbody = document.getElementById('tocbody');
  if (!tbody) return;
  function getCookie(name) {
    var m = new RegExp('(?:^|;\\s*)' + name + '=([^;]*)').exec(document.cookie);
    return m ? decodeURIComponent(m[1]) : '';
  }
  function setCookie(name, value) {
    document.cookie = name + '=' + encodeURIComponent(value) + ';path=/;max-age=31536000';
  }
  var SORTS = {
    'story-desc': ['data-story', true],
    'story-asc': ['data-story', false],
    'pub-desc': ['data-pub', true],
    'pub-asc': ['data-pub', false]
  };
  function applySort(mode) {
    if (!SORTS[mode]) mode = 'story-desc';
    setCookie('rncom_sort', mode);
    var btns = document.querySelectorAll('.sortbtn');
    for (var i = 0; i < btns.length; i++) {
      btns[i].classList.toggle('active', btns[i].getAttribute('data-sort') === mode);
    }
    var attr = SORTS[mode][0], desc = SORTS[mode][1];
    var rows = Array.prototype.slice.call(tbody.querySelectorAll('tr'));
    rows.sort(function (a, b) {
      var ka = a.getAttribute(attr) || '', kb = b.getAttribute(attr) || '';
      return desc ? (ka < kb ? 1 : ka > kb ? -1 : 0) : (ka < kb ? -1 : ka > kb ? 1 : 0);
    });
    rows.forEach(function (r) { tbody.appendChild(r); });
  }
  var btns = document.querySelectorAll('.sortbtn');
  for (var i = 0; i < btns.length; i++) {
    btns[i].addEventListener('click', function () { applySort(this.getAttribute('data-sort')); });
  }
  applySort(getCookie('rncom_sort'));
  var last = getCookie('rncom_last');
  var lr = document.querySelector('.lastread');
  var link = document.getElementById('lastread-link');
  if (last && lr && link) {
    var row = tbody.querySelector('tr[data-story="' + last + '"]');
    if (row) {
      var a = row.querySelector('a');
      if (a) {
        link.href = a.getAttribute('href');
        lr.hidden = false;
      }
    }
  }
})();
</script>
