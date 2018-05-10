# Class to create the HTML and JavaScript to create a map using OpenLayers.

from collections import (
    defaultdict
    )
    

class MapHtml():            
    mapHeight = ""
    mapWidth = ""
    coordinatesDict = defaultdict()

    def html(self):    

        html = """

            <!doctype html>
            <head>
             <script src="http://openlayers.org/en/v4.6.5/build/ol-debug.js"
             type="text/javascript"></script>
             <style>
            .map {
                """
        html = html + "height: " + str(self.mapHeight - 15) + "px;"
        html = html + "width: " + str(self.mapWidth - 15)  + "px;"

        html = html + """
            }
            .tooltip {
              position: relative;
              padding: 3px;
              background: rgba(0, 0, 0, 1);
              color: white;
              opacity: 1;
              white-space: nowrap;
              font: 10pt sans-serif;
            }    
            </style>
            </head>
         
            <body>
            <div id="map" class="map">
              <div id="tooltip" class="tooltip"></div>
            </div>
         
            <script type='text/javascript'>
          
            var map = new ol.Map({
            });
            
            var vectorSource = new ol.source.Vector({});  

            // var map_layer = new ol.layer.Tile({source: new ol.source.OSM({layer: 'osm'})});
            
            var map_layer=new ol.layer.Tile({
                title: "Google Road Map",
                source: new ol.source.TileImage({ url: 'http://mt1.google.com/vt/lyrs=m&x={x}&y={y}&z={z}' }),
            });

            var locationStyle = new ol.style.Style({
              image: new ol.style.Icon({
                  anchor: [1, 1],
                  scale: 1,
                  color: 'red',
                  crossOrigin: 'anonymous',
                  src: 'https://openlayers.org/en/v4.6.5/examples/data/dot.png'
              })
            });    

            var tooltip = document.getElementById('tooltip');
            
            var overlay = new ol.Overlay({
              element: tooltip,
              offset: [-20, 0],
              positioning: 'bottom-left'
            });
            map.addOverlay(overlay);

            function displayTooltip(evt) {
              var pixel = evt.pixel;
              var feature = map.forEachFeatureAtPixel(pixel, function(feature) {
                return feature;
              });
              tooltip.style.display = feature ? '' : 'none';
              if (feature) {
                overlay.setPosition(evt.coordinate);
                tooltip.innerHTML = feature.get('label');
              }
            };

            map.on('pointermove', displayTooltip);

            var vector_layer = new ol.layer.Vector({
                source: vectorSource, 
                style: locationStyle
            });      

            var view = new ol.View({
                center: [0, 0], 
                zoom: 5, 
                maxZoom:18
            });

            map.setTarget('map');
           
            map.setView(view);
             
            map.addLayer(map_layer);
            map.addLayer(vector_layer); 
            
            """

        for c in self.coordinatesDict.keys():
            lat = self.coordinatesDict[c][0]
            long = self.coordinatesDict[c][1]
            label = c
            label = label.replace('"', '')
            html = html + 'var point_feature = new ol.Feature({label: "' + label + '" });'
            html = html + "var pos = ol.proj.fromLonLat([" + long + "," + lat + "]);"
            html = html + """
            var point_geom = new ol.geom.Point(pos);
            point_feature.setGeometry(point_geom);
            vectorSource.addFeature( point_feature );
            
            """

        html = html + """
            var extent = vectorSource.getExtent();

            map.getView().fit(extent, map.getSize());   
         
            </script>
         
            </body>
            </html>
        """

        return(html)
