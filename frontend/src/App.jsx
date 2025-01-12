import React, { Children } from 'react'

import { createBrowserRouter, RouterProvider } from 'react-router-dom';

import Login from './page/Login';
const router=createBrowserRouter(
  [
  
        {
          path:'/',
          element:<Login/>
        }
    
      ]
)
const App = () => {
  return (
    <RouterProvider router={router}/>
  )
}

export default App