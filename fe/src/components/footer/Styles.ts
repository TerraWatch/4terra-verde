import CSS from 'csstype';

const boxStyling: CSS.Properties = { bottom: 0, position: 'absolute', width: '100%', backgroundColor: '#1976d2' };
const titleStyling: CSS.Properties = { flexGrow: 1, color: 'white', textAlign: 'center' };

const Styles =
{
    Box: boxStyling,
    Title: titleStyling
}

export default Styles;