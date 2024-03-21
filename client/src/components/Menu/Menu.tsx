import { FC, useEffect, useState} from "react"

import css from './Menu.module.css'

const Menu: FC = () => {
    const [activeLink, setActiveLink] = useState('');


    useEffect(() => {
      const handleScroll = () => {
        const sections = document.querySelectorAll('section');
        const scrollPosition = window.scrollY;
  
        sections.forEach(section => {
          const top = section.offsetTop;
          const height = section.offsetHeight;
  
          if (scrollPosition >= top && scrollPosition < top + height) {
            setActiveLink(`#${section.id}`);
          }
        });
      };
  
      window.addEventListener('scroll', handleScroll);
      return () => {
        window.removeEventListener('scroll', handleScroll);
      };
    }, []);


    


    



    return (
        <div className={css.menu_container}>
           <div className={css.menu_title}>Start here</div>
           <nav className={css.menu_navigation_container}>
                <a href="#training">
                    <div className={`${css.menu_item} ${activeLink === "#training" ? css.menu_item_active : ""}`}>Training</div>
                </a>
                <a href="#validation">
                    <div className={`${css.menu_item} ${activeLink === "#validation" ? css.menu_item_active : ""}`}>Validation</div>
                </a>
                <a href="#prediction">
                    <div className={`${css.menu_item} ${activeLink === "#prediction" ? css.menu_item_active : ""}`}>Prediction</div>
                </a>
                <a href="#visualization">
                    <div className={`${css.menu_item} ${activeLink === "#visualization" ? css.menu_item_active : ""}`}>Visualization</div>
                </a>
           </nav>
        </div>
    )
}

export { Menu }