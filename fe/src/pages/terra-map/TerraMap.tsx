import { Button, FormControl, InputLabel, MenuItem, Select, SelectChangeEvent, Typography } from '@mui/material';
import { MapContainer, TileLayer } from 'react-leaflet';
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
    
	return (
        <>
            <Typography variant='h6' style={ Styles.Title }>Leaflet Map</Typography>
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