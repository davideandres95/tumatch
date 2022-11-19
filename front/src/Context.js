import React from 'react';

const AuthContext = React.createContext({isAuth:false, token : "", 
                                    setAuth: () => {}})

export default (props) => {
    const [isAuth,setAuth] = React.useState(localStorage.getItem("isAuth") || false)
    const [token, setToken] = React.useState(localStorage.getItem("token"))
    React.useEffect(() => {
        localStorage.setItem("isAuth", isAuth)
        localStorage.setItem("token", token)

    }, [isAuth, token]);
    return (
        <AuthContext.Provider value={{isAuth, setAuth, token, setToken}}>
            {props.children}
        </AuthContext.Provider>
    )
}

export function getContext () {
    return AuthContext;
}