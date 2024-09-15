import GoogleAuthConfig from './configurations/GoogleAuthConfig';
import { GoogleOAuthProvider } from '@react-oauth/google';
import MsAuthConfig from './configurations/MsalConfig';
import { Header } from './components/header/Header';
import { Footer } from './components/footer/Footer';
import { MsalProvider } from '@azure/msal-react';
import { BrowserRouter } from 'react-router-dom';
import { AppRoutes } from './router/AppRoutes';
import { CssBaseline } from '@mui/material';
import React from 'react';

export class App extends React.Component
{
	render(): React.ReactNode
	{
		return (
			<BrowserRouter>
				<CssBaseline/>
				<GoogleOAuthProvider clientId={ GoogleAuthConfig.AuthConfig.clientId }>
					<MsalProvider instance={ MsAuthConfig.AuthConfig }>
						<Header/>
						<AppRoutes/>
						<Footer/>
					</MsalProvider>
				</GoogleOAuthProvider>
			</BrowserRouter>
		)
	}
}