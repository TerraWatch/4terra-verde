import CSS from 'csstype';

const boxStyling: CSS.Properties = { bottom: 0, position: 'absolute', width: '100%', backgroundColor: '#1976d2' };
const drawerButtonStyling: CSS.Properties = { display: 'flex', float: 'inline-start', color: 'white' };
const titleStyling: CSS.Properties = { flex: 1, textAlign: 'center' };

const Styles =
{
    Drawer: drawerButtonStyling,
    Box: boxStyling,
    Title: titleStyling
}

export default Styles;