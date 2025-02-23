import './App.css';
import { useState } from 'react';
import SideBar from './Components/Sidebar/sidebar.js';
import Diary from './Components/Diary/Diary.js';
import Help from './Components/Help/Help.js'; 
import Login from './Components/Login/Login.js';
import Notes from './Components/Notes/notes.js';
import Settings from './Components/Settings/Settings.js';
import Commands from './Components/Commands/commands.js';
import TempLog from './Components/TempLog/Templog.js';
import Eyeball from './assets/Eyeball.png';

function App() {
  const [sidebarOpen, setSidebarOpen] = useState(true);
  const [activeComponent, setActiveComponent] = useState('Diary');

  const toggleSidebar = () => {
    setSidebarOpen(prev => !prev);
  };

  const handleComponentChange = (componentName) => {
    setActiveComponent(componentName);
    setSidebarOpen(false);
  };

  const renderActiveComponent = () => {
    switch (activeComponent) {
      case 'Diary': return <Diary />;
      case 'TempLog': return <TempLog />;
      case 'Help': return <Help />;
      case 'Login': return <Login />;
      case 'Notes': return <Notes />;
      case 'Settings': return <Settings />;
      case 'Commands': return <Commands />;
      default: return <Diary />;
    }
  };

  return (
    <div className="App">
      <div className="logo-toggler-container">
      <img 
        onClick={toggleSidebar} 
        src={Eyeball} 
        className="logo-toggler" 
        alt="Toggle Sidebar"
        style={{ cursor: 'pointer' }}
      />
      </div>

      {sidebarOpen && (
        <SideBar className='SidebarContainer'
          onSetSidebarOpen={setSidebarOpen} 
          onComponentSelect={handleComponentChange} 
        />
      )}
      <div className="active-container">
      {renderActiveComponent()}
      </div>
    </div>
  );
}

export default App;
