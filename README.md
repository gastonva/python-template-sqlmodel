## Original README.md
Go to [xmartlabs/python-template README.md](https://github.com/xmartlabs/python-template/blob/main/README.md)


## SQLModel as an Alternative to SQLAlchemy

This repository provides a simple example to explore the following questions:

- Is SQLModel mature enough for production-like environments?
- How does its performance compare to SQLAlchemy?
- Is SQLModel ready to be used with async/await?

### **SQLModel and Async Support**

As of today (2025-04-01), SQLModel does not natively support `create_async_engine`. More details on this limitation can be found in [`database.py`](https://github.com/gastonva/python-template-sqlmodel/blob/master/src/core/database.py).

### **Conflicts Between SQLModel and SQLAlchemy**

If you are already using SQLAlchemy models and cannot migrate them to SQLModel, you may encounter compatibility issues. For instance:

- SQLAlchemy and SQLModel define models differently, which can lead to conflicts.
- Relationships between SQLAlchemy and SQLModel models are not straightforward.
- Additional adjustments were needed in [`database_sqlmodel.py`](https://github.com/gastonva/python-template-sqlmodel/blob/master/src/core/database_sqlmodel.py) to make both work together.

### **Performance Considerations**

SQLModel inherits from Pydantic, which impacts its performance. A discussion on this topic can be found here: [Slow performance compared to SQLAlchemy using SQLModel for performing group_by operations on a large table #645](https://github.com/fastapi/sqlmodel/discussions/645). The main issue is that SQLModel introduces additional overhead compared to pure SQLAlchemy.

### **Final Thoughts**

Since SQLModel is based on Pydantic—and Pydantic is a standard in FastAPI applications—it can simplify development by making model definitions similar to Pydantic schemas. However, its lack of async support, performance overhead, and compatibility issues with SQLAlchemy models should be carefully considered before using it in production.

## **Resources**

The following resources were used to support this project:

- [SQLModel Official Documentation](https://sqlmodel.tiangolo.com/)
- [GitHub Issues & Discussions on SQLModel:](https://github.com/fastapi/sqlmodel)
  - [Issue #594 - Async Support](https://github.com/fastapi/sqlmodel/issues/594)
  - [Issue #252 - Performance Considerations](https://github.com/fastapi/sqlmodel/issues/252)
  - [Issue #169 - Relationship Handling](https://github.com/fastapi/sqlmodel/issues/169)
  - [Issue #85 - SQLModel Limitations](https://github.com/fastapi/sqlmodel/issues/85)
  - [Issue #330 - Compatibility with SQLAlchemy](https://github.com/fastapi/sqlmodel/issues/330)
  - [Discussion #582 - Best Practices for SQLModel](https://github.com/fastapi/sqlmodel/discussions/582)
- [FastAPI + Alembic + SQLModel Async Example](https://github.com/jonra1993/fastapi-alembic-sqlmodel-async/tree/main)

## **Credits**

This repository is based on work by [Xmartlabs](https://github.com/xmartlabs).
