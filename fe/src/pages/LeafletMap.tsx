import { MapContainer, TileLayer } from 'react-leaflet';
import { Typography } from '@mui/material';
import "leaflet/dist/leaflet.css";
import { useRef } from 'react';

export const LeafletMap = (): JSX.Element =>
{
    const mapReference = useRef(null);
    
	return (
        <>
            <Typography variant='h6' style={ { textAlign: 'center' } }>Leaflet Map</Typography>
            <MapContainer
                center={ [40.6263806, 22.9483502] }
                zoom={ 13 }
                ref={ mapReference }
                style={ { height: '80vh', margin: '10px' } }>
                <TileLayer
                    attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                    url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"/>
            </MapContainer>
        </>
    )
}