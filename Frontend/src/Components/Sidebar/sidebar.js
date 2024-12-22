import React from "react";
import Sidebar from "react-sidebar";
import styles from './sidebar.module.css'; // Ensure you import the updated styles

class SideBar extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      sidebarOpen: true, // Set to true initially
    };
  
    this.onSetSidebarOpen = this.onSetSidebarOpen.bind(this);
  }

  // Toggle sidebar state
  onSetSidebarOpen(open) {
    this.setState({ sidebarOpen: open });
    this.props.onSetSidebarOpen(open); // Update the sidebar state in App
  }

  render() {
    return (
      <>
        {/* Backdrop when sidebar is open */}
        {this.state.sidebarOpen && (
          <div 
            className={styles.backdrop} 
            onClick={() => this.onSetSidebarOpen(false)} 
          />
        )}

        {/* Sidebar component */}
        <Sidebar
          sidebar={
            <div className={styles.SidebarContainer}>
              <ul className={styles.SidebarHead}>
                <li><button onClick={() => {
                  this.onSetSidebarOpen(false);
                  this.props.onComponentSelect('Commands'); // Open Commands component
                }}>Commands</button></li>
                <li><button onClick={() => {
                  this.onSetSidebarOpen(false);
                  this.props.onComponentSelect('Notes'); // Open Notes component
                }}>Notes</button></li>
                <li><button onClick={() => {
                  this.onSetSidebarOpen(false);
                  this.props.onComponentSelect('Diary'); // Open Diary component
                }}>Diary</button></li>
                <li><button onClick={() => {
                  this.onSetSidebarOpen(false);
                  this.props.onComponentSelect('Help'); // Open Help component
                }}>Help</button></li>
                <li><button onClick={() => {
                  this.onSetSidebarOpen(false);
                  this.props.onComponentSelect('Settings'); // Open Settings component
                }}>Settings</button></li>
                <li><button onClick={() => {
                  this.onSetSidebarOpen(false);
                  this.props.onComponentSelect('Login'); // Open Login component
                }}>Login</button></li>
              </ul>
            </div>
          }
          open={this.state.sidebarOpen}
          onSetOpen={this.onSetSidebarOpen}
          styles={{
            sidebar: {
              background: "white",
              height: "100vh",
              width: "15%",
              display: "flex",
              border: "1px solid black",
              padding: "none",
              margin: "none",
              zIndex: 1000
            },
          }}
        />
      </>
    );
  }
}

export default SideBar;