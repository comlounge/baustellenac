
$.fn.sites = (opts = {}) ->

    map_zoom = 13
    max_zoom = 18
    map = L.map('map').setView([50.7753455, 6.0838868], map_zoom)
    markers = {}
    icon_default = L.icon(
        iconUrl: '/static/img/Under_construction_icon-red.svg',
        iconSize: [38, 95],
        popupAnchor: [-3, -76],
        shadowSize: [68, 95],
        shadowAnchor: [22, 94]
    )
    icon_sidewalk = L.icon(
        iconUrl: '/static/img/Under_construction_icon-yellow.svg',
        iconSize: [32, 75],
        popupAnchor: [-3, -76],
        shadowSize: [68, 95],
        shadowAnchor: [22, 94]
    )

    cloudmate_api_key = 'f21ddba0627f45a7820c966a23ca9002'
    map_url = 'http://{s}.tile.cloudmade.com/'+cloudmate_api_key+'/997/256/{z}/{x}/{y}.png'
    map_attribution = 'Map data &copy; <a href="http://openstreetmap.org">OpenStreetMap</a> contributors, <a href="http://creativecommons.org/licenses/by-sa/2.0/">CC-BY-SA</a>, Imagery © <a href="http://cloudmade.com">CloudMade</a>'


    init = () ->
        L.tileLayer(map_url, {
            attribution: map_attribution,
            maxZoom: max_zoom
        }).addTo(map)

        $('.site').each(() ->
            make_marker($(this))
        )

        $('.site').click(() ->
            markers[$(this).data('id')].openPopup()
        )

        map.on('popupopen', () ->
            $('.moreinfo').click( (e) ->
                show_infomodal($(this).data('id'))
            )
        )

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
        adr = data['sections'][0]['street']+', '+data['sections'][0]['zip']+' '+data['sections'][0]['city']
        address = $('<div class="row"></div>')
            .append('<div class="span2">Adresse</div>')
            .append('<div class="span4">'+adr+'</div>')

        m.find('.modal-body').html('')
        m.find('.modal-body')
            .append(subtitle)
            .append(desc)
            .append(organisation)
            .append(approx_time)
            .append(start_time)
            .append(end_time)
            .append(address)

    make_marker = (elem) ->
        start_lat = elem.data('start_lat')
        start_lng = elem.data('start_lng')
        end_lat = elem.data('end_lat')
        end_lng = elem.data('end_lng')

        if start_lat != 'None' and start_lng != 'None'
            if end_lat != 'None' and end_lng != 'None'
                lat = (start_lat + end_lat)/2
                lng = (start_lng + end_lng)/2
                #make_route(start_lat,start_lng,end_lat,end_lng)
            else
                lat = start_lat
                lng = start_lng

            icon = icon_default
            if elem.data('sidewalk_only') == 'True'
                icon = icon_sidewalk

            console.log(elem.data('sidewalk_only'))

            marker = L.marker([lat, lng], {icon: icon}).addTo(map)
            markers[elem.data('id')] = marker
            marker.bindPopup(make_infopopup(elem))


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

    $(this).each(init)
    this



$(document).ready( () ->

    $("body").sites();

)

