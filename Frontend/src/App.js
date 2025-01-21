import './App.css';
import { useState } from 'react';
import SideBar from './Components/Sidebar/sidebar.js';
import Diary from './Components/Diary/Diary.js';
import Help from './Components/Help/Help.js'; 
import Login from './Components/Login/Login.js'; // Import Login component
import Notes from './Components/Notes/notes.js'; // Import Notes component
import Settings from './Components/Settings/Settings.js'; // Import Settings component
import Commands from './Components/Commands/commands.js'; // Import Commands component
import TempLog from './Components/TempLog/Templog.js'; //

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [activeComponent, setActiveComponent] = useState('Diary'); // Set initial active component

  const toggleSidebar = () => {
    setSidebarOpen((prev) => !prev); // Toggle the sidebar state
  };

  // Function to change the active component and close the sidebar
  const handleComponentChange = (componentName) => {
    setActiveComponent(componentName);
    setSidebarOpen(false); // Close the sidebar after selecting a component
  };

  // Render the active component dynamically
  const renderActiveComponent = () => {
    switch (activeComponent) {
      case 'Diary':
        return <Diary />;
      case 'TempLog':
        return <TempLog />;
      case 'Help':
        return <Help />;
      case 'Login':
        return <Login />;
      case 'Notes':
        return <Notes />;
      case 'Settings':
        return <Settings />;
      case 'Commands':
        return <Commands />;
      default:
        return <Diary />;
    }
  };

  return (
    <div className="App">

            {/* Button to toggle the sidebar */}
            <button onClick={toggleSidebar} className='sidebarButton'>
        {sidebarOpen ? 'Close Sidebar' : 'Open Sidebar'}
      </button>
      {/* Conditionally render the SideBar based on its state */}
      {sidebarOpen && (
        <SideBar className='SidebarContainer'
          onSetSidebarOpen={setSidebarOpen} 
          onComponentSelect={handleComponentChange} // Pass the function to change component
        />
      )}

      {/* Render the active component dynamically */}
      {renderActiveComponent()}

    </div>
  );
}

export default App;