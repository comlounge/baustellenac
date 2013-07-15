
$.fn.sites = (opts = {}) ->

    map_zoom = 15
    max_zoom = 18
    default_lat = 50.7753455
    default_lng = 6.0838868
    map = null
    staticmap = null
    marker = null
    smarker = null

    icon_default = L.icon(
        iconUrl: '/static/img/Under_construction_icon-red.svg',
        iconSize: [38, 95],
        popupAnchor: [0, -15],
        shadowSize: [68, 95],
        shadowAnchor: [22, 94]
    )
    icon_sidewalk = L.icon(
        iconUrl: '/static/img/Under_construction_icon-yellow.svg',
        iconSize: [32, 75],
        popupAnchor: [0, -15],
        shadowSize: [68, 95],
        shadowAnchor: [22, 94]
    )
    icon = null

    map_url = $("body").data("tileurl")
    map_attribution = 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>, Baustellendaten der <a href="http://aachen.de/baustellen">Stadt Aachen</a>. Informationen ohne Gewähr.'


    init = () ->
        init_icon()
        init_static_map()
        $('.showmap').click( ()->
            $('#mapmodal').modal('show')
            init_edit_map()
        )

    init_icon = () ->
        if $('#site-form').data('sidewalk_only') == 'True'
            icon = icon_sidewalk
        else
            icon = icon_default

    init_edit_map = ()->
        lat = $('#siteconfig').data('lat')
        lng = $('#siteconfig').data('lng')
        if lat == '' or lng == ''
            lat = default_lat
            lng = default_lng
        map = L.map('map',
            center: [lat, lng]
            zoom: map_zoom
        )
        L.tileLayer(map_url, {
            attribution: map_attribution,
            maxZoom: max_zoom
        }).addTo(map)
        map.on('click', set_marker);
        if lat != default_lat
            marker = L.marker([lat, lng],
                draggable:true
                icon:icon
            )
            marker.on('dragend', set_marker_latlng_to_form)
            map.addLayer(marker)

    init_static_map = ()->
        lat = $('#siteconfig').data('lat')
        lng = $('#siteconfig').data('lng')
        if lat == '' or lng == ''
            lat = default_lat
            lng = default_lng
        staticmap = L.map('staticmap',
            zoom: 16
            center: [lat,lng]
            dragging: false
            scrollWheelZoom: false
            doubleClickZoom: false
            zoomControl: false
        )
        L.tileLayer(map_url, {
            maxZoom: max_zoom
        }).addTo(staticmap)
        if lat != default_lat
            set_static_marker([lat,lng])

    set_marker = (e)->
        if marker != null
            map.removeLayer(marker)
        marker = L.marker(e.latlng,
            draggable:true
            icon:icon
        )
        marker.on('dragend', set_marker_latlng_to_form)
        map.addLayer(marker)
        set_marker_latlng_to_form()

    set_static_marker = (latlng)->
        if smarker != null
            staticmap.removeLayer(smarker)
        smarker = L.marker(latlng,
            draggable:false
            clickable:false
            icon:icon
        )
        staticmap.addLayer(smarker)
        staticmap.panTo(latlng)

    set_marker_latlng_to_form = ()->
        lat = marker.getLatLng().lat
        lng = marker.getLatLng().lng
        $('input[name=lat]').val(lat)
        $('input[name=lng]').val(lng)
        set_static_marker([lat,lng])




    $(this).each(init)
    this



$(document).ready( () ->

    $("body").sites();

)

