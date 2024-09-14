import { BrowserRouter } from 'react-router-dom';
import { AppRoutes } from './router/AppRoutes';
import { Header } from './components/Header';
import { Footer } from './components/Footer';
import { CssBaseline } from '@mui/material';
import React from 'react';

export class App extends React.Component
{
	render(): React.ReactNode
	{
		return (
			<BrowserRouter>
				<CssBaseline/>
				<Header/>
				<AppRoutes/>
				<Footer/>
			</BrowserRouter>
		)
	}
}