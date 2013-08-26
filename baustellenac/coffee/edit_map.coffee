
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
        iconSize: [38, 38],
        popupAnchor: [0, -15],
        shadowSize: [68, 95],
        shadowAnchor: [22, 94]
    )
    icon_sidewalk = L.icon(
        iconUrl: '/static/img/Under_construction_icon-yellow.svg',
        iconSize: [32, 32],
        popupAnchor: [0, -15],
        shadowSize: [68, 95],
        shadowAnchor: [22, 94]
    )
    icon = null

    map_url = $("body").data("tileurl")
    map_attribution = 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>, Baustellendaten der <a href="http://aachen.de/baustellen">Stadt Aachen</a>. Informationen ohne Gewähr.'


    init = () ->
        init_icon()
        init_marker_polyline()
        $('.showmap').click( (event)->
            $('#mapmodal').modal('show')
            if not map
                init_edit_map()
            false
        )
        init_static_map()

        $('input#sidewalk_only').on('change', ()->
            if $('input#sidewalk_only').attr('checked') == 'checked'
                icon = icon_sidewalk
            else
                icon = icon_default
            if marker?
                marker.setIcon(icon)
            if smarker?
                smarker.setIcon(icon)
        )

        # init street search in edit map view
        $('#streetsselect').select2(
            placeholder: "Suchen Sie nach einer Strasse..."
            allowClear: true
            openOnEnter: true
        )
        $('#streetsselect').on('keydown', (e) ->
            $('#streetsselect').select2('open')
        )
        $('#streetsselect').on('change', (e) ->
            street_latlng = JSON.parse($('#streetsselect').val())
            if marker != null
                drawnItems.removeLayer(marker)
            marker = L.marker(street_latlng,
                draggable:true
                icon:icon
            )
            drawnItems.addLayer(marker)
            map.panTo(street_latlng)
            set_marker_latlng_to_form()
            set_static_marker()
        )

        # modal events
        $('#mapmodal').on('shown', () ->
            $('#streetsselect').focus()
        )
        $('#mapmodal').on('hidden', () ->
            set_marker_latlng_to_form()
            set_static_marker()
            # set polyline form data
            $('#polyline').val(JSON.stringify(polyline.getLatLngs()))
            set_static_polyline()
        )

    init_icon = () ->
        if $('#siteconfig').data('sidewalk_only') == 'True'
            icon = icon_sidewalk
        else
            icon = icon_default

    init_marker_polyline = ()->
        lat = $('#siteconfig').data('lat')
        lng = $('#siteconfig').data('lng')
        if lat? and lng?
            marker = L.marker([lat,lng],
                draggable:true
                icon:icon
            )
        pl_latlngs = $('#siteconfig').data('polyline')
        if pl_latlngs?
            polyline = L.polyline(pl_latlngs,
                clickable: true
                weight: 10
            )

    init_edit_map = ()->
        if marker?
            latlng = marker.getLatLng()
        else
            latlng = [default_lat,default_lng]
        map = L.map('map',
            center: latlng
            zoom: map_zoom
        )
        L.tileLayer(map_url, {
            attribution: map_attribution,
            maxZoom: max_zoom
        }).addTo(map)

        drawnItems = new L.FeatureGroup()
        # set marker if found
        if marker?
            drawnItems.addLayer(marker)
        # draw polyline if found
        if polyline?
            drawnItems.addLayer(polyline)

        map.addLayer(drawnItems)
        # Initialize the draw control and pass it the FeatureGroup of editable layers
        drawControl = new L.Control.Draw(
            position: 'topleft'
            draw:
                marker:
                    draggable:true
                    icon: icon
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
                layer.options.draggable = true
            if type == 'polyline'
                #drawnItems.removeLayer(polyline)
                polyline = layer
                layer.options.weight = 10
            drawnItems.addLayer(layer)
        )

    init_static_map = ()->
        if marker?
            latlng = marker.getLatLng()
        else
            latlng = [default_lat,default_lng]
        staticmap = L.map('staticmap',
            zoom: 16
            center: latlng
            dragging: false
            scrollWheelZoom: false
            doubleClickZoom: false
            zoomControl: false
        )
        L.tileLayer(map_url, {
            maxZoom: max_zoom
        }).addTo(staticmap)
        if marker?
            set_static_marker()
        if polyline?
            set_static_polyline()

    set_static_marker = ()->
        if smarker != null
            staticmap.removeLayer(smarker)
        if marker?
            smarker = L.marker(marker.getLatLng(),
                draggable:false
                clickable:false
                icon:icon
            )
            staticmap.addLayer(smarker)
            staticmap.panTo(marker.getLatLng())

    set_static_polyline = ()->
        if spolyline?
            staticmap.removeLayer(spolyline)
        if polyline?
            spolyline = L.polyline(polyline.getLatLngs(), weight:10);
            staticmap.addLayer(spolyline)

    set_marker_latlng_to_form = ()->
        if marker?
            $('input[name=lat]').val(marker.getLatLng().lat)
            $('input[name=lng]').val(marker.getLatLng().lng)


    $(this).each(init)
    this


$.fn.mapsearch = (opts = {}) ->

    $this = $(this)

    init = () ->

    $(this).each(init)
    this


$(document).ready( () ->

    $("#streetsselect").mapsearch()

    $("body").sites()

    # editing organisation (Träger)
    $('#organisation_add_button').click(()->
        $('#organisationmodal').modal('show')
        $('#organisation-name').val('')
        $('#organisation-name').focus()

        $('#organisation-name').keypress((e)->
            if e.which == 13
                $('#organisation_add').focus()
                submit_organisation()
                $('#organisationmodal').modal('hide')
        )

    )
    $('#organisation_add').click(()->
        submit_organisation()
    )
    submit_organisation = () ->
        if $('#organisation-name').val() != ''
            $.ajax(
                url: "/organisation/add"
                type: 'POST'
                data:
                    name: $('#organisation-name').val()
                error: (data) ->
                    console.log 'error'
                success: (data) ->
                    $('#organisation')
                    .append($("<option></option>")
                        .attr("value",data['name'])
                        .text(data['name'])
                    )
                    $('#organisation').val(data['name'])
            )

)

