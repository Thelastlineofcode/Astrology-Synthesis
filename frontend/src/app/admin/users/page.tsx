"use client";

import React, { useState, useEffect } from "react";
import AdminSidebar from "../../../components/admin/AdminSidebar";
import "./page.css";

interface User {
  id: string;
  email: string;
  name: string;
  role: "user" | "admin";
}

const UserManagement = () => {
  const [users, setUsers] = useState<User[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [showCreateModal, setShowCreateModal] = useState(false);
  const [editingUser, setEditingUser] = useState<User | null>(null);

  const [formData, setFormData] = useState({
    email: "",
    name: "",
    password: "",
    role: "user" as "user" | "admin",
  });

  const fetchUsers = async () => {
    try {
      setLoading(true);
      // TODO: Replace with actual API call
      // For now, show mock data
      setUsers([
        {
          id: "1",
          email: "admin@roots-revealed.com",
          name: "Admin User",
          role: "admin",
        },
        { id: "2", email: "user@example.com", name: "John Doe", role: "user" },
      ]);
      setLoading(false);
    } catch (err) {
      setError("Failed to fetch users");
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchUsers();
  }, []);

  const handleCreateUser = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      // TODO: Replace with actual API call
      console.log("Creating user:", {
        email: formData.email,
        name: formData.name,
        role: formData.role,
      });
      setShowCreateModal(false);
      resetForm();
      fetchUsers();
    } catch (err) {
      setError("Failed to create user");
    }
  };

  const handleUpdateUser = async (e: React.FormEvent) => {
    e.preventDefault();
    try {
      // TODO: Replace with actual API call
      console.log("Updating user:", editingUser?.id, {
        email: formData.email,
        name: formData.name,
        role: formData.role,
      });
      setEditingUser(null);
      resetForm();
      fetchUsers();
    } catch (err) {
      setError("Failed to update user");
    }
  };

  const handleDeleteUser = async (userId: string) => {
    if (!confirm("Are you sure you want to delete this user?")) return;

    try {
      // TODO: Replace with actual API call
      console.log("Deleting user:", userId);
      fetchUsers();
    } catch (err) {
      setError("Failed to delete user");
    }
  };

  const resetForm = () => {
    setFormData({
      email: "",
      name: "",
      password: "",
      role: "user",
    });
  };

  const startEdit = (user: User) => {
    setEditingUser(user);
    setFormData({
      email: user.email,
      name: user.name,
      password: "",
      role: user.role,
    });
  };

  return (
    <div className="admin-layout">
      <AdminSidebar userName="Admin User" />

      <div className="admin-content">
        <header className="admin-header">
          <div className="admin-header-top">
            <h1 className="admin-title">User Management</h1>
            <button
              className="create-button"
              onClick={() => setShowCreateModal(true)}
            >
              + Create User
            </button>
          </div>
        </header>

        <div className="admin-main">
          {error && (
            <div className="error-message">
              {error}
              <button onClick={() => setError(null)}>×</button>
            </div>
          )}

          {loading ? (
            <div className="loading">Loading users...</div>
          ) : (
            <div className="users-table-container">
              <table className="users-table">
                <thead>
                  <tr>
                    <th>Name</th>
                    <th>Email</th>
                    <th>Role</th>
                    <th>Actions</th>
                  </tr>
                </thead>
                <tbody>
                  {users.map((user) => (
                    <tr key={user.id}>
                      <td>{user.name}</td>
                      <td>{user.email}</td>
                      <td>
                        <span className={`role-badge role-badge--${user.role}`}>
                          {user.role}
                        </span>
                      </td>
                      <td>
                        <div className="action-buttons">
                          <button
                            className="action-button action-button--edit"
                            onClick={() => startEdit(user)}
                          >
                            Edit
                          </button>
                          <button
                            className="action-button action-button--delete"
                            onClick={() => handleDeleteUser(user.id)}
                          >
                            Delete
                          </button>
                        </div>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          )}
        </div>
      </div>

      {(showCreateModal || editingUser) && (
        <div
          className="modal-overlay"
          onClick={() => {
            setShowCreateModal(false);
            setEditingUser(null);
            resetForm();
          }}
        >
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <div className="modal-header">
              <h2>{editingUser ? "Edit User" : "Create User"}</h2>
              <button
                className="modal-close"
                onClick={() => {
                  setShowCreateModal(false);
                  setEditingUser(null);
                  resetForm();
                }}
              >
                ×
              </button>
            </div>
            <form onSubmit={editingUser ? handleUpdateUser : handleCreateUser}>
              <div className="form-group">
                <label htmlFor="name">Name</label>
                <input
                  type="text"
                  id="name"
                  value={formData.name}
                  onChange={(e) =>
                    setFormData({ ...formData, name: e.target.value })
                  }
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor="email">Email</label>
                <input
                  type="email"
                  id="email"
                  value={formData.email}
                  onChange={(e) =>
                    setFormData({ ...formData, email: e.target.value })
                  }
                  required
                />
              </div>
              <div className="form-group">
                <label htmlFor="password">
                  Password {editingUser && "(leave blank to keep current)"}
                </label>
                <input
                  type="password"
                  id="password"
                  value={formData.password}
                  onChange={(e) =>
                    setFormData({ ...formData, password: e.target.value })
                  }
                  required={!editingUser}
                  minLength={6}
                />
              </div>
              <div className="form-group">
                <label htmlFor="role">Role</label>
                <select
                  id="role"
                  value={formData.role}
                  onChange={(e) =>
                    setFormData({
                      ...formData,
                      role: e.target.value as "user" | "admin",
                    })
                  }
                  required
                >
                  <option value="user">User</option>
                  <option value="admin">Admin</option>
                </select>
              </div>
              <div className="modal-actions">
                <button
                  type="button"
                  className="button button--secondary"
                  onClick={() => {
                    setShowCreateModal(false);
                    setEditingUser(null);
                    resetForm();
                  }}
                >
                  Cancel
                </button>
                <button type="submit" className="button button--primary">
                  {editingUser ? "Update" : "Create"}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

export default UserManagement;
