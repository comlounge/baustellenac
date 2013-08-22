
$.fn.sites = (opts = {}) ->

    map_zoom = 13
    max_zoom = 18
    current_zoom = 16
    map = L.map('map',
        center: [50.7753455, 6.0838868]
        zoom: map_zoom
    )
    markers = {}
    polyline = null
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

    map_url = $("body").data("tileurl")
    map_attribution = 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>, Baustellendaten von der <a href="http://aachen.de/baustellen">Stadt Aachen</a>. Informationen ohne Gewähr.'


    init = () ->
        L.tileLayer(map_url, {
            attribution: map_attribution,
            maxZoom: max_zoom
        }).addTo(map)

        $('.site').each(() ->
            make_marker($(this))
        )

        $('.site').click(() ->
            if markers.hasOwnProperty($(this).data('id'))
                map.panTo(markers[$(this).data('id')].getLatLng(), {'animate':true})
                map.setZoom(current_zoom, {'animate':true})
                markers[$(this).data('id')].openPopup()
            show_polyline($(this))
        )
        #$('.site').on('mouseout', on_site_out)
        #$('.site').click(() ->
        #    show_infomodal($(this).data('id'))
        #)

        map.locate({setView: true, maxZoom: 2})
        map.on('locationfound', onLocationFound)

        map.on('popupopen', () ->
            $('.moreinfo').click( (e) ->
                show_infomodal($(this).data('id'))
            )
        )

    onLocationFound = (e) ->
        radius = e.accuracy / 2;
        L.marker(e.latlng).addTo(map)
            .bindPopup("You are within " + radius + " meters from this point").openPopup()
        L.circle(e.latlng, radius).addTo(map)


    show_infomodal = (sid) ->
        path = '/api/site/'+sid+'.json'
        $.ajax(
            url: path,
            dataType: 'json',
            success: (data) ->
                create_infomodal(data)
                $('#infomodal').modal('show')
            ,
            error: () ->
                alert("Error");
            ,
        )

    create_infomodal = (data) ->
        m = $('#infomodal')
        m.find('.modal-header h3').html(data['name'])

        body = ""
        subtitle = $('<div class="row"></div>')
            .append('<div class="span2">Untertitel</div>')
            .append('<div class="span4">'+data['subtitle']+'</div>')
        desc = $('<div class="row"></div>')
            .append('<div class="span2">Beschreibung</div>')
            .append('<div class="span4">'+data['description']+'</div>')
        organisation = $('<div class="row"></div>')
            .append('<div class="span2">Träger</div>')
            .append('<div class="span4">'+data['organisation']+'</div>')
        approx_time = $('<div class="row"></div>')
            .append('<div class="span2">Vorr. Zeitrahmen</div>')
            .append('<div class="span4">'+data['approx_timeframe']+'</div>')
        start_date = new Date(data['start_date'])
        start_time = $('<div class="row"></div>')
            .append('<div class="span2">Beginn</div>')
            .append('<div class="span4">'+start_date.toLocaleDateString('de')+'</div>')
        end_date = new Date(data['end_date'])
        end_time = $('<div class="row"></div>')
            .append('<div class="span2">Ende</div>')
            .append('<div class="span4">'+end_date.toLocaleDateString('de')+'</div>')
        #adr = data['sections'][0]['street']+', '+data['sections'][0]['zip']+' '+data['sections'][0]['city']
        #address = $('<div class="row"></div>')
        #    .append('<div class="span2">Adresse</div>')
        #    .append('<div class="span4">'+adr+'</div>')

        m.find('.modal-body').html('')
        m.find('.modal-body')
            .append(subtitle)
            .append(desc)
            .append(organisation)
            .append(approx_time)
            .append(start_time)
            .append(end_time)
            #.append(address)

    make_marker = (elem) ->
        lat = elem.data('lat')
        lng = elem.data('lng')

        if lat != '' and lng != ''
            icon = icon_default
            if elem.data('sidewalk_only') == 'True'
                icon = icon_sidewalk

            marker = L.marker([lat, lng], {icon: icon}).addTo(map)
            markers[elem.data('id')] = marker
            marker.bindPopup(make_infopopup(elem))
            marker.on('click', ()->
                show_polyline(elem)
            )
            #marker.on('mouseout', remove_polyline)


    make_infopopup = (elem) ->
        info = '<b>'+elem.data('name')+'</b>'
        if elem.data('sidewalk_only') == 'True'
            info += ' (Nur auf dem Gehweg)'
        info += '<br/>'
        if elem.data('subtitle')
            info += elem.data('subtitle')+'<br/><br/>'
        else
            info += '<br/>'
        info += 'Träger: '+elem.data('organisation')+'<br/>'
        info += 'Vorr. Dauer: '+elem.data('approx_timeframe')+'<br/><br/>'
        info += '<button class="moreinfo" type="button" data-id="'+elem.data('id')+'">Mehr Informationen</button>'
        #info += '<a href="#" class="pull-right">mehr...</a><br/>'
        info

    make_route = (start_lat,start_lng,end_lat,end_lng) ->
        routing_url = "http://routes.cloudmade.com/f21ddba0627f45a7820c966a23ca9002/api/0.3/"+start_lat+","+start_lng+","+end_lat+","+end_lng+"/foot.js?lang=de&units=km"
        $.ajax(
            url:routing_url,
            dataType: 'jsonp',
            success: (data) ->
                if data['status'] == 0
                    polyline = L.polyline(data.route_geometry, {color:'red'}).addTo(map)
            ,
            error: () ->
                alert("Error");
            ,
        )

    show_polyline = (elem) ->
        remove_polyline()
        pl_latlngs = elem.data('polyline')
        if pl_latlngs
            polyline = L.polyline(pl_latlngs,
                clickable: true
            ).addTo(map)

    on_site_over = (elem, marker) ->
        #for k of markers
        #    if markers[k] != marker
        #        markers[k].setOpacity(0.5)
        show_polyline(elem)

    remove_polyline = ()->
        #for k of markers
        #    markers[k].setOpacity(1)
        if polyline and map.hasLayer(polyline)
            map.removeLayer(polyline)

    $(this).each(init)
    this



$(document).ready( () ->

    $("body").sites();

)

