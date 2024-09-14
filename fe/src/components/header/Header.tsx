import { Box, AppBar, Toolbar, Typography, Button, Menu, MenuItem, Divider, Drawer, List, ListItem, ListItemButton, ListItemIcon, ListItemText } from '@mui/material';
import { Dashboard, Map, Info, Google, Email } from '@mui/icons-material';
import { useGoogleLogin } from '@react-oauth/google';
import { useNavigate } from 'react-router-dom';
import React, { SyntheticEvent } from 'react';
import { useMsal } from '@azure/msal-react';
import Styles from './Styles';
import axios from 'axios';

const LogInMethods =
[
	{ id: 'btnMsLogin', caption: 'Microsoft', icon: <Email fontSize="small"/> },
	{ id: 'btnGoogleLogin', caption: 'Google', icon: <Google fontSize="small"/> }
];

const DrawerItems =
[
	{ id: 'btnDashboard', caption: 'Dashboard', icon: <Dashboard/> },
	{ id: 'btnAbout', caption: 'About', icon: <Info/> },
	{ id: 'btnOlmap', caption: 'OpenLayer Map', icon: <Map/> },
	{ id: 'btnLmap', caption: 'Leaflet Map', icon: <Map/> }
]

export const Header = () =>
{
	const navigate = useNavigate();
	const { instance } = useMsal();

	const [anchorElement, setAnchorElement] = React.useState<HTMLElement | null>(null);
	const [drawerOpen, setDrawerOpen] = React.useState<boolean>(false);
	const [, setUser] = React.useState<any | null>(null);
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
			case 'btnLmap': navigate('map');
				break;
			case 'btnMsLogin': microsoftLogin();
				break;
			case 'btnGoogleLogin': googleLogin();
				break;
		}
		setAnchorElement(null);
	}

	const handleLoginMenuClick = (event: React.MouseEvent<HTMLButtonElement>): void => setAnchorElement(event.currentTarget);

	const handleClose = (): void => setAnchorElement(null);

	const toggleDrawer = (newOpen: boolean) => (): void => setDrawerOpen(newOpen);

	const microsoftLogin = () =>
	{
		setAnchorElement(null);
		instance
			.loginPopup()
			.then(setUser)
			.catch(console.error);
	};

	const googleLogin = useGoogleLogin(
	{
		onSuccess: response => axios
			.get(`https://www.googleapis.com/oauth2/v1/userinfo?access_token=${response.access_token}`)
			.then(setUser)
			.catch(console.error),
		onError: console.error
	});

	return (
		<Box sx={{ flexGrow: 1 }}>
			<AppBar position='static'>
				<Toolbar>
					<Typography variant='h6' component='div' style={ Styles.Title } onClick={ toggleDrawer(true) }>TerraWatch</Typography>
					<Button color='inherit' onClick={ handleLoginMenuClick }>Log In</Button>
					<Menu anchorEl={ anchorElement } open={ menuOpen } onClose={ handleClose }>
						{
							LogInMethods.map(lim =>
							(
								<MenuItem key={ lim.id } id={ lim.id } onClick={ handleClick }>
									<ListItemIcon>{ lim.icon }</ListItemIcon>{ lim.caption }
								</MenuItem>
							))
						}
					</Menu>
				</Toolbar>
			</AppBar>
			<Drawer open={ drawerOpen } onClose={ toggleDrawer(false) }>
				<Box sx={{ width: 250 }} role="presentation" onClick={ toggleDrawer(false) }>
					<List>
						{
							DrawerItems.map(di =>
							(
								<ListItem key={ di.caption } disablePadding>
									<ListItemButton id={ di.id } onClick={ handleClick }>
										<ListItemIcon>
											{ di.icon }
										</ListItemIcon>
										<ListItemText primary={ di.caption }/>
									</ListItemButton>
								</ListItem>
							))
						}
					</List>
				</Box>
			</Drawer>
		</Box>
	);
}