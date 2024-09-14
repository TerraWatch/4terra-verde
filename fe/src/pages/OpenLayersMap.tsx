import { Typography } from '@mui/material';
import TileLayer from 'ol/layer/Tile.js';
import OSM from 'ol/source/OSM.js';
import { useEffect } from 'react';
import * as proj from "ol/proj";
import View from 'ol/View.js';
import Map from 'ol/Map.js';
import 'ol/ol.css';

export const OpenLayersMap = (): JSX.Element =>
{
    const hellas = proj.fromLonLat([22.9483502, 40.6263806]);
    
    useEffect(() =>
    {
        const olMap = new Map(
        {
            target: 'map',
            layers: [ new TileLayer({ source: new OSM() }) ],
            view: new View({ center: [0, 0], zoom: 13 })
        });
        olMap.getView().animate({ zoom: 13 }, { center: hellas }, { duration: 2000 });
    }, []);
    
    return (
        <>
            <Typography variant='h6' style={ { textAlign: 'center' } }>OpenLayers Map</Typography>
            <div id="map" style={ { height: '80vh', margin: '10px' } }></div>
        </>
    )
}