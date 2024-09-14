import { Box, Typography } from '@mui/material';
import CSS from 'csstype';
import React from 'react';

const boxStyling: CSS.Properties = { bottom: 0, position: 'absolute', width: '100%', backgroundColor: '#1976d2' };
const titleStyling: CSS.Properties = { flexGrow: 1, color: 'white', textAlign: 'center' };

export class Footer extends React.Component
{
	render(): React.ReactNode
    {
		return (
			<Box sx={ boxStyling }>
                <Typography variant='h6' component='div' sx={ titleStyling }>TerraWatch</Typography>
			</Box>
		)
	}
}