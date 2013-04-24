
$.fn.sites = (opts = {}) ->

    map_zoom = 13
    max_zoom = 18
    map = L.map('map').setView([50.7753455, 6.0838868], map_zoom)

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

    make_marker = (elem) ->
        start_lat = elem.data('start_lat')
        start_lng = elem.data('start_lng')
        end_lat = elem.data('end_lat')
        end_lng = elem.data('end_lng')

        start_marker = L.marker([start_lat, start_lng]).addTo(map)
        #end_marker = L.marker([start_lat, end_lng]).addTo(map)

        info = '<b>'+elem.data('name')+'</b><br/><br/>'
        info += elem.data('description')+'<br/><br/>'
        info += 'Träger: '+elem.data('organisation')+'<br/><br/>'
        info += 'Vorr. Dauer: '+elem.data('approx_timeframe')
        start_marker.bindPopup(info)

        #make_route(start_lat,start_lng,end_lat,end_lng)

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

