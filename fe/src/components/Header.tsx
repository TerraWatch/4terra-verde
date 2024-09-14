import { Box, AppBar, Toolbar, Typography, Button, Menu, MenuItem, Divider, Drawer, List, ListItem, ListItemButton, ListItemIcon, ListItemText } from '@mui/material';
import { Dashboard, Map, Info, Google, Email } from '@mui/icons-material';
import { useGoogleLogin } from '@react-oauth/google';
import { useNavigate } from 'react-router-dom';
import React, { SyntheticEvent } from 'react';
import { useMsal } from '@azure/msal-react';
import axios from 'axios';

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
			case 'btnLmap': navigate('lmap');
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
					<Typography variant='h6' component='div' style={ { flex: 1, cursor: 'pointer' } } onClick={ toggleDrawer(true) }>TerraWatch</Typography>
					<Button color='inherit' onClick={ handleLoginMenuClick }>Log In</Button>
					<Menu anchorEl={ anchorElement } open={ menuOpen } onClose={ handleClose }>
						<MenuItem id='btnMsLogin' onClick={ handleClick }>
							<ListItemIcon>
								<Email fontSize="small"/>
							</ListItemIcon>
							Microsoft
						</MenuItem>
						<MenuItem id='btnGoogleLogin' onClick={ handleClick }>
							<ListItemIcon>
								<Google fontSize="small"/>
							</ListItemIcon>
							Google
						</MenuItem>
					</Menu>
				</Toolbar>
			</AppBar>
			<Drawer open={ drawerOpen } onClose={ toggleDrawer(false) }>
				<Box sx={{ width: 250 }} role="presentation" onClick={ toggleDrawer(false) }>
					<List>
						<ListItem key='Dashboard' disablePadding>
							<ListItemButton id='btnDashboard' onClick={ handleClick }>
								<ListItemIcon>
									<Dashboard/>
								</ListItemIcon>
								<ListItemText primary='Dashboard'/>
							</ListItemButton>
						</ListItem>
						<ListItem key='About' disablePadding>
							<ListItemButton id='btnAbout' onClick={ handleClick }>
								<ListItemIcon>
									<Info/>
								</ListItemIcon>
								<ListItemText primary='About'/>
							</ListItemButton>
						</ListItem>
					</List>
					<Divider/>
					<List>
						<ListItem key='OpenLayer Map' disablePadding>
							<ListItemButton id='btnOlmap' onClick={ handleClick }>
								<ListItemIcon>
									<Map/>
								</ListItemIcon>
								<ListItemText primary='OpenLayer Map'/>
							</ListItemButton>
						</ListItem>
						<ListItem key='Leaflet Map' disablePadding>
							<ListItemButton id='btnLmap' onClick={ handleClick }>
								<ListItemIcon>
									<Map/>
								</ListItemIcon>
								<ListItemText primary='Leaflet Map'/>
							</ListItemButton>
						</ListItem>
					</List>
				</Box>
			</Drawer>
		</Box>
	);
}