
$.fn.sites = (opts = {}) ->

    map_zoom = 15
    max_zoom = 18
    default_lat = 50.7753455
    default_lng = 6.0838868
    map = null
    staticmap = null
    marker = null
    smarker = null
    drawControl = null
    drawnItems = null
    polyline = null
    spolyline = null

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
        lat = $('#siteconfig').data('lat')
        lng = $('#siteconfig').data('lng')
        pl_latlngs = $('#siteconfig').data('polyline')
        if not lat? or not lng? or lat == '' or lng == ''
            lat = default_lat
            lng = default_lng
        $('.showmap').click( ()->
            $('#mapmodal').modal('show')
            if not map
                init_edit_map(lat,lng,pl_latlngs)
        )

    init_icon = () ->
        if $('#site-form').data('sidewalk_only') == 'True'
            icon = icon_sidewalk
        else
            icon = icon_default

    init_edit_map = (lat,lng, pl_latlngs)->
        map = L.map('map',
            center: [lat, lng]
            zoom: map_zoom
        )
        L.tileLayer(map_url, {
            attribution: map_attribution,
            maxZoom: max_zoom
        }).addTo(map)

        drawnItems = new L.FeatureGroup()
        # set marker if found
        if lat != default_lat and lng != default_lng
            marker = L.marker([lat,lng],
                draggable:false
                clickable:false
                icon:icon
            )
            drawnItems.addLayer(marker)
        # draw polyline if found
        if pl_latlngs
            polyline = L.polyline(pl_latlngs,
                clickable: true
            )
            drawnItems.addLayer(polyline)

        map.addLayer(drawnItems)
        # Initialize the draw control and pass it the FeatureGroup of editable layers
        drawControl = new L.Control.Draw(
            position: 'topleft'
            draw:
                marker: {
                    icon: icon
                }
                polygon: false
                circle: false
                rectangle: false
            edit:
                featureGroup: drawnItems
                edit: false
        )
        map.addControl(drawControl)
        map.on('draw:created', (e) ->
            type = e.layerType
            layer = e.layer
            if type == 'marker'
                drawnItems.removeLayer(marker)
                marker = layer
                # set marker form data
                set_marker_latlng_to_form()
                # set marker on static map
                set_static_marker([marker.getLatLng().lat, marker.getLatLng().lng])
            if type == 'polyline'
                drawnItems.removeLayer(polyline)
                polyline = layer
                # set polyline form data
                $('#polyline').val(JSON.stringify(polyline._latlngs))
                # set polyline on static map
                set_static_polyline(polyline._latlngs)
            drawnItems.addLayer(layer)
        )

    init_static_map = ()->
        lat = $('#siteconfig').data('lat')
        lng = $('#siteconfig').data('lng')
        platlngs = $('#siteconfig').data('polyline')
        console.log(lat)
        console.log(lng)
        console.log(poloyline?)
        if not lat? or not lng? or lat == '' or lng == ''
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
        if platlngs?
            set_static_polyline(platlngs)

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

    set_static_polyline = (latlngs)->
        if spolyline?
            staticmap.removeLayer(spolyline)
        spolyline = L.polyline(latlngs);
        staticmap.addLayer(spolyline)

    set_marker_latlng_to_form = ()->
        lat = marker.getLatLng().lat
        lng = marker.getLatLng().lng
        $('input[name=lat]').val(lat)
        $('input[name=lng]').val(lng)


    $(this).each(init)
    this



$(document).ready( () ->

    $("body").sites();

)

