import { Typography } from '@mui/material';
import TileLayer from 'ol/layer/Tile.js';
import OSM from 'ol/source/OSM.js';
import { useEffect } from 'react';
import * as proj from "ol/proj";
import Styles from './Styles';
import View from 'ol/View.js';
import Map from 'ol/Map.js';
import 'ol/ol.css';

export const OpenLayersMap = (): JSX.Element =>
{
    const hellas = proj.fromLonLat([22.62, 40.54]);
    
    useEffect(() =>
    {
        const olMap = new Map(
        {
            target: 'map',
            layers: [ new TileLayer({ source: new OSM() }) ],
            view: new View({ center: [0, 0], zoom: 11 })
        });
        olMap.getView().animate({ zoom: 11 }, { center: hellas }, { duration: 2000 });
    }, []);
    
    return (
        <>
            <Typography variant='h6' style={ Styles.Title }>OpenLayers Map</Typography>
            <div id="map" style={ Styles.Map }></div>
        </>
    )
}