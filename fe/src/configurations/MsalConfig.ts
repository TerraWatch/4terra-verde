import { PublicClientApplication } from '@azure/msal-browser';

const tenantId = '#TENANT_ID#';

const AuthConfig =
{
    auth:
    {
        clientId: '#CLIENT_ID#',
        authorityId: `https://login.microsoftonline.com/${tenantId}`,
        redirectUri: 'http://localhost:3000'
    },
    cache:
    {
        cacheLocation: 'sessionStorage',
        storeAuthStateInCookie: false
    }
};

const LoginRequest = { scopes: ['User.Read'] };

const GraphConfig = { graphMeEndpoint: 'https://graph.microsoft.com/v1.0/me' };

const MsAuthConfig =
{
    AuthConfig: new PublicClientApplication(AuthConfig),
    LoginRequest,
    GraphConfig
};

export default MsAuthConfig;