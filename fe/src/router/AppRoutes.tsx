import { OpenLayersMap } from '../pages/OpenLayersMap';
import { Route, Routes } from 'react-router-dom';
import { LeafletMap } from '../pages/LeafletMap';
import { Dashboard } from '../pages/Dashboard';
import { About } from '../pages/About';
import { ReactNode } from 'react';
import React from 'react';

export class AppRoutes extends React.Component
{
    render(): ReactNode
    {
        return (
            <Routes>
                <Route path='/' Component={ Dashboard }/>
                <Route path='/about' Component={ About }/>
                <Route path='/olmap' Component={ OpenLayersMap }/>
                <Route path='/lmap' Component={ LeafletMap }/>
            </Routes>
        )
    }
}