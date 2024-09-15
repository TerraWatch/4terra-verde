import { Box, Typography } from '@mui/material';
import Styles from './Styles';
import React from 'react';

export class Footer extends React.Component
{
	render(): React.ReactNode
    {
		return (
			<Box sx={ Styles.Box }>
                <Typography variant='body1' component='div' sx={ Styles.Title }>TerraWatch</Typography>
			</Box>
		)
	}
}