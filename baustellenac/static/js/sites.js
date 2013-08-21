// Generated by CoffeeScript 1.4.0

$.fn.sites = function(opts) {
  var create_infomodal, icon_default, icon_sidewalk, init, make_infopopup, make_marker, make_route, map, map_attribution, map_url, map_zoom, markers, max_zoom, onLocationFound, on_site_out, on_site_over, polyline, show_infomodal, show_polyline;
  if (opts == null) {
    opts = {};
  }
  map_zoom = 13;
  max_zoom = 18;
  map = L.map('map', {
    center: [50.7753455, 6.0838868],
    zoom: map_zoom
  });
  markers = {};
  polyline = null;
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
  map_url = $("body").data("tileurl");
  map_attribution = 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>, Baustellendaten von der <a href="http://aachen.de/baustellen">Stadt Aachen</a>. Informationen ohne Gewähr.';
  init = function() {
    L.tileLayer(map_url, {
      attribution: map_attribution,
      maxZoom: max_zoom
    }).addTo(map);
    $('.site').each(function() {
      return make_marker($(this));
    });
    $('.site').mouseover(function() {
      if (markers.hasOwnProperty($(this).data('id'))) {
        markers[$(this).data('id')].openPopup();
      }
      return on_site_over($(this), markers[$(this).data('id')]);
    });
    $('.site').on('mouseout', on_site_out);
    $('.site').click(function() {
      return show_infomodal($(this).data('id'));
    });
    map.locate({
      setView: true,
      maxZoom: 2
    });
    map.on('locationfound', onLocationFound);
    return map.on('popupopen', function() {
      return $('.moreinfo').click(function(e) {
        return show_infomodal($(this).data('id'));
      });
    });
  };
  onLocationFound = function(e) {
    var radius;
    radius = e.accuracy / 2;
    L.marker(e.latlng).addTo(map).bindPopup("You are within " + radius + " meters from this point").openPopup();
    return L.circle(e.latlng, radius).addTo(map);
  };
  show_infomodal = function(sid) {
    var path;
    path = '/api/site/' + sid + '.json';
    return $.ajax({
      url: path,
      dataType: 'json',
      success: function(data) {
        create_infomodal(data);
        return $('#infomodal').modal('show');
      },
      error: function() {
        return alert("Error");
      }
    });
  };
  create_infomodal = function(data) {
    var approx_time, body, desc, end_date, end_time, m, organisation, start_date, start_time, subtitle;
    m = $('#infomodal');
    m.find('.modal-header h3').html(data['name']);
    body = "";
    subtitle = $('<div class="row"></div>').append('<div class="span2">Untertitel</div>').append('<div class="span4">' + data['subtitle'] + '</div>');
    desc = $('<div class="row"></div>').append('<div class="span2">Beschreibung</div>').append('<div class="span4">' + data['description'] + '</div>');
    organisation = $('<div class="row"></div>').append('<div class="span2">Träger</div>').append('<div class="span4">' + data['organisation'] + '</div>');
    approx_time = $('<div class="row"></div>').append('<div class="span2">Vorr. Zeitrahmen</div>').append('<div class="span4">' + data['approx_timeframe'] + '</div>');
    start_date = new Date(data['start_date']);
    start_time = $('<div class="row"></div>').append('<div class="span2">Beginn</div>').append('<div class="span4">' + start_date.toLocaleDateString('de') + '</div>');
    end_date = new Date(data['end_date']);
    end_time = $('<div class="row"></div>').append('<div class="span2">Ende</div>').append('<div class="span4">' + end_date.toLocaleDateString('de') + '</div>');
    m.find('.modal-body').html('');
    return m.find('.modal-body').append(subtitle).append(desc).append(organisation).append(approx_time).append(start_time).append(end_time);
  };
  make_marker = function(elem) {
    var icon, lat, lng, marker;
    lat = elem.data('lat');
    lng = elem.data('lng');
    if (lat !== '' && lng !== '') {
      icon = icon_default;
      if (elem.data('sidewalk_only') === 'True') {
        icon = icon_sidewalk;
      }
      marker = L.marker([lat, lng], {
        icon: icon
      }).addTo(map);
      markers[elem.data('id')] = marker;
      marker.bindPopup(make_infopopup(elem));
      marker.on('mouseover', function() {
        return on_site_over(elem, marker);
      });
      return marker.on('mouseout', on_site_out);
    }
  };
  make_infopopup = function(elem) {
    var info;
    info = '<b>' + elem.data('name') + '</b>';
    if (elem.data('sidewalk_only') === 'True') {
      info += ' (Nur auf dem Gehweg)';
    }
    info += '<br/>';
    if (elem.data('subtitle')) {
      info += elem.data('subtitle') + '<br/><br/>';
    } else {
      info += '<br/>';
    }
    info += 'Träger: ' + elem.data('organisation') + '<br/>';
    info += 'Vorr. Dauer: ' + elem.data('approx_timeframe') + '<br/><br/>';
    info += '<button class="moreinfo" type="button" data-id="' + elem.data('id') + '">Mehr Informationen</button>';
    return info;
  };
  make_route = function(start_lat, start_lng, end_lat, end_lng) {
    var routing_url;
    routing_url = "http://routes.cloudmade.com/f21ddba0627f45a7820c966a23ca9002/api/0.3/" + start_lat + "," + start_lng + "," + end_lat + "," + end_lng + "/foot.js?lang=de&units=km";
    return $.ajax({
      url: routing_url,
      dataType: 'jsonp',
      success: function(data) {
        if (data['status'] === 0) {
          return polyline = L.polyline(data.route_geometry, {
            color: 'red'
          }).addTo(map);
        }
      },
      error: function() {
        return alert("Error");
      }
    });
  };
  show_polyline = function(elem) {
    var pl_latlngs;
    pl_latlngs = elem.data('polyline');
    if (pl_latlngs) {
      return polyline = L.polyline(pl_latlngs, {
        clickable: true
      }).addTo(map);
    }
  };
  on_site_over = function(elem, marker) {
    var k;
    for (k in markers) {
      if (markers[k] !== marker) {
        markers[k].setOpacity(0.5);
      }
    }
    return show_polyline(elem);
  };
  on_site_out = function() {
    var k;
    for (k in markers) {
      markers[k].setOpacity(1);
    }
    if (map.hasLayer(polyline)) {
      return map.removeLayer(polyline);
    }
  };
  $(this).each(init);
  return this;
};

$(document).ready(function() {
  return $("body").sites();
});
