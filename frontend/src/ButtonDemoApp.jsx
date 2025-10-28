import React from 'react';
import ReactDOM from 'react-dom/client';
import ButtonDemo from './components/shared/ButtonDemo';
import './components/shared/Button.css';
import './components/shared/ButtonDemo.css';

const root = ReactDOM.createRoot(document.getElementById('root'));
root.render(
  <React.StrictMode>
    <ButtonDemo />
  </React.StrictMode>
);
