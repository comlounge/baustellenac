// Generated by CoffeeScript 1.4.0

$.fn.sites = function(opts) {
  var default_lat, default_lng, icon, icon_default, icon_sidewalk, init, init_edit_map, init_icon, init_static_map, map, map_attribution, map_url, map_zoom, marker, max_zoom, set_marker, set_marker_latlng_to_form, set_static_marker, smarker, staticmap;
  if (opts == null) {
    opts = {};
  }
  map_zoom = 15;
  max_zoom = 18;
  default_lat = 50.7753455;
  default_lng = 6.0838868;
  map = null;
  staticmap = null;
  marker = null;
  smarker = null;
  icon_default = L.icon({
    iconUrl: '/static/img/Under_construction_icon-red.svg',
    iconSize: [38, 95],
    popupAnchor: [0, -15],
    shadowSize: [68, 95],
    shadowAnchor: [22, 94]
  });
  icon_sidewalk = L.icon({
    iconUrl: '/static/img/Under_construction_icon-yellow.svg',
    iconSize: [32, 75],
    popupAnchor: [0, -15],
    shadowSize: [68, 95],
    shadowAnchor: [22, 94]
  });
  icon = null;
  map_url = $("body").data("tileurl");
  map_attribution = 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>, Baustellendaten der <a href="http://aachen.de/baustellen">Stadt Aachen</a>. Informationen ohne Gewähr.';
  init = function() {
    init_icon();
    init_static_map();
    return $('.showmap').click(function() {
      $('#mapmodal').modal('show');
      return init_edit_map();
    });
  };
  init_icon = function() {
    if ($('#site-form').data('sidewalk_only') === 'True') {
      return icon = icon_sidewalk;
    } else {
      return icon = icon_default;
    }
  };
  init_edit_map = function() {
    var lat, lng;
    lat = $('#siteconfig').data('lat');
    lng = $('#siteconfig').data('lng');
    if (lat === '' || lng === '') {
      lat = default_lat;
      lng = default_lng;
    }
    map = L.map('map', {
      center: [lat, lng],
      zoom: map_zoom
    });
    L.tileLayer(map_url, {
      attribution: map_attribution,
      maxZoom: max_zoom
    }).addTo(map);
    map.on('click', set_marker);
    if (lat !== default_lat) {
      marker = L.marker([lat, lng], {
        draggable: true,
        icon: icon
      });
      marker.on('dragend', set_marker_latlng_to_form);
      return map.addLayer(marker);
    }
  };
  init_static_map = function() {
    var lat, lng;
    lat = $('#siteconfig').data('lat');
    lng = $('#siteconfig').data('lng');
    if (lat === '' || lng === '') {
      lat = default_lat;
      lng = default_lng;
    }
    staticmap = L.map('staticmap', {
      zoom: 16,
      center: [lat, lng],
      dragging: false,
      scrollWheelZoom: false,
      doubleClickZoom: false,
      zoomControl: false
    });
    L.tileLayer(map_url, {
      maxZoom: max_zoom
    }).addTo(staticmap);
    if (lat !== default_lat) {
      return set_static_marker([lat, lng]);
    }
  };
  set_marker = function(e) {
    if (marker !== null) {
      map.removeLayer(marker);
    }
    marker = L.marker(e.latlng, {
      draggable: true,
      icon: icon
    });
    marker.on('dragend', set_marker_latlng_to_form);
    map.addLayer(marker);
    return set_marker_latlng_to_form();
  };
  set_static_marker = function(latlng) {
    if (smarker !== null) {
      staticmap.removeLayer(smarker);
    }
    smarker = L.marker(latlng, {
      draggable: false,
      clickable: false,
      icon: icon
    });
    staticmap.addLayer(smarker);
    return staticmap.panTo(latlng);
  };
  set_marker_latlng_to_form = function() {
    var lat, lng;
    lat = marker.getLatLng().lat;
    lng = marker.getLatLng().lng;
    $('input[name=lat]').val(lat);
    $('input[name=lng]').val(lng);
    return set_static_marker([lat, lng]);
  };
  $(this).each(init);
  return this;
};

$(document).ready(function() {
  return $("body").sites();
});
