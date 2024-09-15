import { Button, FormControl, InputLabel, MenuItem, Select, SelectChangeEvent, Typography } from '@mui/material';
import { Circle, CircleMarker, MapContainer, Marker, Polyline, Popup, TileLayer } from 'react-leaflet';
import { SyntheticEvent, useRef } from 'react';
import Grid from '@mui/material/Grid2';
import "leaflet/dist/leaflet.css";
import Styles from './Styles';
import React from 'react';

const TrainingAlgorithms =
[
    { key: 'soc', value: 'Soil Organic Carbon' },
    { key: 'da', value: 'Deforestation / Afforestation' }
]

export const TerraMap = (): JSX.Element =>
{
    const [trainingAlgorithm, setTrainingAlgorithm] = React.useState<string>('');
    const mapReference = useRef(null);

    const trainingAlgorithmSelected = (e: SelectChangeEvent) => setTrainingAlgorithm(e.target.value);

    const getLayer = (e: SyntheticEvent) => console.log(e);

    const polyline: [number, number][] =
    [
        [40.55, 22.60],
        [40.60, 22.63],
        [40.58, 22.68],
        [40.55, 22.60]
    ];
    
	return (
        <>
            <Typography variant='h6' style={ Styles.Title }>Map</Typography>
            <Grid container>
                <Grid size={ 6 }>
                    <MapContainer
                        center={ [40.54, 22.62] }
                        zoom={ 10 }
                        ref={ mapReference }
                        style={ Styles.Map }>
                        <TileLayer
                            attribution='&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors'
                            url="https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png"/>
                        <Circle center={ [40.44, 22.52] } pathOptions={ { fillColor: 'blue' } } radius={2000}>
                            <Popup>Blue Area</Popup>
                        </Circle>
                        <CircleMarker center={ [40.64, 22.52] } pathOptions={ { color: 'red' } } radius={20}>
                            <Popup>Red Area</Popup>
                        </CircleMarker>
                        <Polyline pathOptions={ { color: 'lime' } } positions={ polyline }>
                            <Popup>Lime Polyline</Popup>
                        </Polyline>
                    </MapContainer>
                </Grid>
                <Grid size={ 6 }>
                    <Grid container sx={ { margin: 2 } }>
                        <Grid size={ 12 } sx={ { flexGrow: 1 } }>
                            <FormControl fullWidth size='small'>
                                <InputLabel>Layer</InputLabel>
                                <Select label='Layer' value={ trainingAlgorithm } onChange={ trainingAlgorithmSelected }>
                                    { TrainingAlgorithms.map(ta => (<MenuItem key={ ta.value } value={ ta.key }>{ ta.value }</MenuItem>)) }
                                </Select>
                            </FormControl>
                            <Button variant='contained' color='success' sx={ { float: 'inline-end', margin: 1 } } onClick={ getLayer }>Get Layer</Button>
                        </Grid>
                    </Grid>
                </Grid>
            </Grid>
        </>
    )
}