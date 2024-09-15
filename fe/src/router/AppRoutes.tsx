import { OpenLayersMap } from '../pages/open-layers-map/OpenLayersMap';
import { Dashboard } from '../pages/dashboard/Dashboard';
import { TerraMap } from '../pages/terra-map/TerraMap';
import { Route, Routes } from 'react-router-dom';
import { About } from '../pages/about/About';
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
                <Route path='/map' Component={ TerraMap }/>
            </Routes>
        )
    }
}