
$.fn.sites = (opts = {}) ->

    map_zoom = 13
    max_zoom = 18
    map = L.map('map').setView([50.7753455, 6.0838868], map_zoom)
    markers = {}

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
                console.log(data)
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
        desc = $('<div class="row"></div>')
            .append('<div class="span2">Bescreibung</div>')
            .append('<div class="span4">'+data['description']+'</div>')
        organisation = $('<div class="row"></div>')
            .append('<div class="span2">Träger</div>')
            .append('<div class="span4">'+data['organisation']+'</div>')
        approx_time = $('<div class="row"></div>')
            .append('<div class="span2">Vorr. Zeitrahmen</div>')
            .append('<div class="span4">'+data['approx_timeframe']+'</div>')

        m.find('.modal-body').html('')
        m.find('.modal-body').append(desc)
        m.find('.modal-body').append(organisation)
        m.find('.modal-body').append(approx_time)

        console.log(desc)

    make_marker = (elem) ->
        start_lat = elem.data('start_lat')
        start_lng = elem.data('start_lng')
        end_lat = elem.data('end_lat')
        end_lng = elem.data('end_lng')

        start_marker = L.marker([start_lat, start_lng]).addTo(map)
        markers[elem.data('id')] = start_marker
        #end_marker = L.marker([start_lat, end_lng]).addTo(map)

        start_marker.bindPopup(make_infopopup(elem))

        #make_route(start_lat,start_lng,end_lat,end_lng)

    make_infopopup = (elem) ->
        info = '<b>'+elem.data('name')+'</b><br/><br/>'
        info += elem.data('description')+'<br/><br/>'
        info += 'Träger: '+elem.data('organisation')+'<br/><br/>'
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

