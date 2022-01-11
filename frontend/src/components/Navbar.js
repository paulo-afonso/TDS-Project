import React from 'react';
import { ReactComponent as Logo } from '../assets/logo-nav.svg';
import '../styles/navbar.css';

const Navbar = () => {
    return (
        <header className='header'>
            <nav>
                <Logo />
                <div className='menu'>
                    <a href='#'>sobre</a>
                    <a href='#'>strateegia</a>
                </div>
            </nav>
        </header> 
    )
};

export default Navbar;
