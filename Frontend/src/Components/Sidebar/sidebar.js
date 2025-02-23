import React, { useState, useEffect, useRef } from "react";
import Sidebar from "react-sidebar";
import styles from './sidebar.module.css';

const SideBar = ({ onSetSidebarOpen, onComponentSelect }) => {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [menuItems, setMenuItems] = useState([
    { name: "Commands", key: "Commands" },
    { name: "Notes", key: "Notes" },
    { name: "Diary", key: "Diary" },
    { name: "TempLog", key: "TempLog" },
    { name: "Help", key: "Help" },
    { name: "Settings", key: "Settings" },
    { name: "Login", key: "Login" },
  ]);

  const sidebarRef = useRef(null);

  // Function to toggle sidebar state
  const handleSetSidebarOpen = (open) => {
    setSidebarOpen(open);
    onSetSidebarOpen(open);
  };

  // Infinite scrolling effect
  const handleScroll = () => {
    if (sidebarRef.current) {
      const { scrollTop, scrollHeight, clientHeight } = sidebarRef.current;
      
      // If at the bottom, reorder items
      if (scrollTop + clientHeight >= scrollHeight - 1) { // Small buffer to trigger earlier
        setMenuItems((prevItems) => {
          const newItems = [...prevItems];
          const firstItem = newItems.shift(); // Remove first item
          newItems.push(firstItem); // Add to bottom

          return newItems;
        });

        // Maintain smooth scrolling by resetting scroll position slightly
        setTimeout(() => {
          sidebarRef.current.scrollTop -= 40; // Prevents jump effect
        }, 0);
      }
    }
  };

  useEffect(() => {
    const sidebar = sidebarRef.current;
    if (sidebar) {
      sidebar.addEventListener("scroll", handleScroll);
    }
    return () => {
      if (sidebar) {
        sidebar.removeEventListener("scroll", handleScroll);
      }
    };
  }, []);

  return (
    <>
      {sidebarOpen && (
        <div className={styles.backdrop} onClick={() => handleSetSidebarOpen(false)} />
      )}

      <Sidebar
        sidebar={
          <div className={styles.SidebarContainer} ref={sidebarRef} style={{ overflowY: "auto", height: "100vh" }}>
            <ul className={styles.SidebarHead}>
              {menuItems.map((item, index) => (
                <li key={index}>
                  <button
                    onClick={() => {
                      handleSetSidebarOpen(false);
                      onComponentSelect(item.key);
                    }}
                  >
                    {item.name}
                  </button>
                </li>
              ))}
            </ul>
          </div>
        }
        open={sidebarOpen}
        onSetOpen={handleSetSidebarOpen}
        styles={{
          sidebar: {
            background: "white",
            height: "100vh",
            width: "15%",
            display: "flex",
            border: "1px solid black",
            zIndex: 1000,
            overflowY: "hidden", // Ensure internal container handles scroll
          },
        }}
      />
    </>
  );
};

export default SideBar;
