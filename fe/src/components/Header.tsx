import { Box, AppBar, Toolbar, Typography, Button, Menu, MenuItem } from '@mui/material';
import { useNavigate } from 'react-router-dom';
import React, { SyntheticEvent } from 'react';

export const Header = () =>
{
	const navigate = useNavigate();

	const [anchorElement, setAnchorElement] = React.useState<null | HTMLElement>(null);
	const menuOpen = Boolean(anchorElement);

	const handleClick = (e: SyntheticEvent): void =>
	{
		switch (e.currentTarget.id)
		{
			case 'btnDashboard': navigate('/');
				break;
			case 'btnAbout': navigate('about');
				break;
			case 'btnOlmap': navigate('olmap');
				break;
			case 'btnLmap': navigate('lmap');
				break;
		}
		setAnchorElement(null);
	}

	const handleMapsMenuClick = (event: React.MouseEvent<HTMLButtonElement>): void => setAnchorElement(event.currentTarget);

	const handleClose = (): void => setAnchorElement(null);

	return (
		<Box sx={{ flexGrow: 1 }}>
			<AppBar position='static'>
				<Toolbar>
					<Typography variant='h6' component='div' style={ { flex: 1 } }>TerraWatch</Typography>
					<Button id='btnDashboard' color='inherit' onClick={ handleClick }>Dashboard</Button>
					<Button id='btnAbout' color='inherit' onClick={ handleClick }>About</Button>
					<Button color='inherit' onClick={ handleMapsMenuClick }>Maps</Button>
					<Menu anchorEl={ anchorElement } open={ menuOpen } onClose={ handleClose }>
						<MenuItem id='btnOlmap' onClick={ handleClick }>OpenLayers Map</MenuItem>
						<MenuItem id='btnLmap' onClick={ handleClick }>Leaflet Map</MenuItem>
					</Menu>
				</Toolbar>
			</AppBar>
		</Box>
	);
}