"use client";

import React, { useState } from 'react';
import AdminSidebar from '../../components/admin/AdminSidebar';
import DashboardWidget from '../../components/admin/DashboardWidget';
import './page.css';

const AdminDashboard = () => {
  const [activeTab, setActiveTab] = useState('general');

  const tabs = [
    { id: 'general', label: 'General' },
    { id: 'studies', label: 'Studies' },
    { id: 'finance', label: 'Finance' },
    { id: 'teaching', label: 'Teaching' },
  ];

  const todoItems = [
    'Dep SNAP Benefits 17',
    'Citizenship Status 17',
    'Other Untax Income Dependent 17',
  ];

  const holdItems = [
    'Dep SNAP Benefits 17',
    'Citizenship Status 17',
    'Other Untax Income Dependent 17',
  ];

  const advisees = [
    {
      id: '1',
      name: 'Luis Arcos',
      code: 'AA0004',
      phone: '(480) 250 1555',
      email: 'larcos@highpoint.com',
    },
    {
      id: '2',
      name: 'Madison Peterson',
      code: 'AA0027',
      phone: '(480) 250 1555',
      email: 'larcos@highpoint.com',
    },
  ];

  const inboxMessages = [
    {
      id: '1',
      title: 'Class Meeting Changes',
      date: 'April 12, 2019, 8:00 am',
    },
    {
      id: '2',
      title: 'Class Meeting Changes',
      date: 'April 12, 2019, 8:00 am',
    },
    {
      id: '3',
      title: 'Class Meeting Changes',
      date: 'April 12, 2019, 8:00 am',
    },
  ];

  return (
    <div className="admin-layout">
      <AdminSidebar userName="George" />
      
      <div className="admin-content">
        <header className="admin-header">
          <div className="admin-header-top">
            <h1 className="admin-title">Dashboard</h1>
            <button className="settings-button" aria-label="Settings">
              ⚙️
            </button>
          </div>
        </header>

        <div className="admin-main">
          <div className="greeting-section">
            <h2 className="greeting">Hello George! 👋</h2>
            
            <div className="tabs">
              {tabs.map((tab) => (
                <button
                  key={tab.id}
                  className={`tab ${activeTab === tab.id ? 'tab--active' : ''}`}
                  onClick={() => setActiveTab(tab.id)}
                >
                  {tab.label}
                </button>
              ))}
              <button className="edit-widgets-button">
                ⚙️ Edit My Widgets
              </button>
            </div>
          </div>

          <div className="dashboard-grid">
            <div className="dashboard-row">
              <div className="dashboard-col">
                <DashboardWidget
                  title="To Dos"
                  headerAction={
                    <button className="icon-button" aria-label="Open in new window">
                      ↗
                    </button>
                  }
                >
                  <ul className="widget-list">
                    {todoItems.map((item, index) => (
                      <li key={index} className="widget-list-item">
                        <span className="widget-list-item-text">{item}</span>
                        <span className="widget-list-item-arrow">›</span>
                      </li>
                    ))}
                  </ul>
                  <a href="#" className="widget-link">View 5 More</a>
                </DashboardWidget>
              </div>

              <div className="dashboard-col">
                <DashboardWidget
                  title="Holds"
                  headerAction={
                    <button className="icon-button" aria-label="Open in new window">
                      ↗
                    </button>
                  }
                >
                  <ul className="widget-list">
                    {holdItems.map((item, index) => (
                      <li key={index} className="widget-list-item">
                        <span className="widget-list-item-text">{item}</span>
                        <span className="widget-list-item-arrow">›</span>
                      </li>
                    ))}
                  </ul>
                </DashboardWidget>
              </div>
            </div>

            <div className="dashboard-row">
              <div className="dashboard-col">
                <DashboardWidget
                  title="Shopping Cart 2019 Spring"
                  headerAction={
                    <button className="icon-button" aria-label="Open in new window">
                      ↗
                    </button>
                  }
                >
                  <div className="shopping-cart-grid">
                    <div className="course-card">
                      <div className="course-name">General Biology I</div>
                      <div className="course-code">ACCT 201-1301</div>
                      <button className="course-button">Open</button>
                    </div>
                    <div className="course-card">
                      <div className="course-name">Financial Accounting</div>
                      <div className="course-code">ACCT 201-1301</div>
                      <button className="course-button">Open</button>
                    </div>
                    <div className="course-card">
                      <div className="course-name">Yoga</div>
                      <div className="course-code">ACCT 201-1301</div>
                      <button className="course-button">Open</button>
                    </div>
                  </div>
                </DashboardWidget>
              </div>

              <div className="dashboard-col">
                <DashboardWidget
                  title="Advisees"
                  headerAction={
                    <button className="icon-button" aria-label="Open in new window">
                      ↗
                    </button>
                  }
                >
                  <div className="advisees-grid">
                    {advisees.map((advisee) => (
                      <div key={advisee.id} className="advisee-card">
                        <div className="advisee-avatar">
                          {advisee.name.charAt(0)}
                        </div>
                        <div className="advisee-info">
                          <div className="advisee-name">{advisee.name}</div>
                          <div className="advisee-code">{advisee.code}</div>
                          <div className="advisee-contact">
                            <span>📞 {advisee.phone}</span>
                          </div>
                          <div className="advisee-contact">
                            <span>✉️ {advisee.email}</span>
                          </div>
                          <button className="advisee-button">Act as a user</button>
                        </div>
                      </div>
                    ))}
                  </div>
                </DashboardWidget>
              </div>
            </div>

            <div className="dashboard-row">
              <div className="dashboard-col">
                <DashboardWidget
                  title="Waitlist 2019 Spring"
                  headerAction={
                    <button className="icon-button" aria-label="Open in new window">
                      ↗
                    </button>
                  }
                >
                  <div className="waitlist-content">
                    <div className="waitlist-item">
                      <div className="waitlist-course">
                        <div className="course-name">Financial Accounting I</div>
                        <div className="course-code">ACCT 201 - 2001 (1697)</div>
                      </div>
                      <div className="waitlist-status">
                        <div className="status-row">
                          <span className="status-label">Status:</span>
                          <span className="status-value">Waiting</span>
                        </div>
                        <div className="status-row">
                          <span className="status-label">Position:</span>
                          <span className="status-value">1</span>
                        </div>
                      </div>
                      <button className="course-button">Open</button>
                    </div>
                  </div>
                </DashboardWidget>
              </div>

              <div className="dashboard-col">
                <DashboardWidget
                  title="Inbox"
                  headerAction={
                    <button className="icon-button" aria-label="Open in new window">
                      ↗
                    </button>
                  }
                >
                  <ul className="widget-list">
                    {inboxMessages.map((message) => (
                      <li key={message.id} className="widget-list-item inbox-item">
                        <div>
                          <div className="inbox-title">✉️ {message.title}</div>
                          <div className="inbox-date">{message.date}</div>
                        </div>
                        <span className="widget-list-item-arrow">›</span>
                      </li>
                    ))}
                  </ul>
                  <a href="#" className="widget-link">View 23 More</a>
                </DashboardWidget>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};

export default AdminDashboard;
