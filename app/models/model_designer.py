from sqlalchemy import Column, Integer, String, Float, ForeignKey
from app.models.database_connectivity import Base
from sqlalchemy.orm import relationship


class Country(Base):
    __tablename__ = "country"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True, nullable=False)

    dashboard = relationship(
        "AIDrivenInsightsDashboard",
        back_populates="country",
        uselist=False,
        cascade="all, delete-orphan"
    )

    # One-to-many with states
    states = relationship(
        "DashboardState",
        back_populates="country",
        cascade="all, delete-orphan"
    )

    def __repr__(self):
        return f"<Country(id={self.id}, name={self.name})>"


class DashboardState(Base):
    __tablename__ = "dashboard_state"

    id = Column(Integer, primary_key=True, autoincrement=True)
    country_id = Column(Integer, ForeignKey("country.id"), nullable=False)
    state_name = Column(String(100), nullable=False, index=True)
    percentage = Column(Float, nullable=True)
    country = relationship("Country", back_populates="states")

    def __repr__(self):
        return f"<State(id={self.id}, state={self.state_name}, percentage={self.percentage}, country_id={self.country_id})>"


class AIDrivenInsightsDashboard(Base):
    __tablename__ = "ai_driven_insights_dashboard"

    id = Column(Integer, primary_key=True, autoincrement=True)
    country_id = Column(Integer, ForeignKey("country.id"), unique=True, nullable=False)
    total_loans = Column(Integer, nullable=True)
    total_balance = Column(Float, nullable=True)
    wac = Column(Float, nullable=True)
    conc_loan_type = Column(String(100), nullable=True)
    conc_geography = Column(String(100), nullable=True)
    conc_credit_tier = Column(String(100), nullable=True)
    portfolio_reliability_score = Column(String(100), nullable=True)
    document_quality_score = Column(Float, nullable=True)
    percent_outliers = Column(Float, nullable=True)
    split_single_family = Column(Float, nullable=True)
    split_condo = Column(Float, nullable=True)
    split_multi_family = Column(Float, nullable=True)
    risk_ltv_gt_80 = Column(Float, nullable=True)
    risk_dti_gt_43 = Column(Float, nullable=True)
    no_qc = Column(Float, nullable=True)
    country = relationship("Country", back_populates="dashboard")

    def __repr__(self):
        return f"<Dashboard(id={self.id}, loans={self.total_loans}, balance={self.total_balance}, country={self.country_id})>"


class PortfolioLevelInsightsWidget(Base):
    __tablename__ = "portfolio_level_insights_widgets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    delinquency_percent = Column(Float, nullable=False)
    epd_percent = Column(Float, nullable=False)
    score = Column(Float, nullable=False)
    watchlist = Column(String, nullable=True)
    recommendation = Column(String, nullable=True)

    def __repr__(self):
        return f"<PortfolioLevelInsightsWidget(id={self.id}, score={self.score})>"


class PortfolioLevelData(Base):
    __tablename__ = "portfolio_level_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pool_number = Column(String, nullable=False)  # keeping as string for flexibility
    average_fico = Column(Float, nullable=False)
    weighted_avg_ltv = Column(Float, nullable=False)
    weighted_avg_dti = Column(Float, nullable=False)
    delinquency_percent = Column(Float, nullable=False)
    epd_percent = Column(Float, nullable=False)  # Early Payments Default
    weighted_collateral_score = Column(Float, nullable=False)
    red_flag = Column(String, nullable=True)

    def __repr__(self):
        return f"<PortfolioLevelData(pool={self.pool_number}, fico={self.average_fico})>"


class PoolLevelInsightsWidget(Base):
    __tablename__ = "pool_level_insights_widgets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    delinquency_percent = Column(Float, nullable=False)
    epd_percent = Column(Float, nullable=False)
    score = Column(Float, nullable=False)
    watchlist_outliers = Column(String, nullable=True)  # e.g., "12 loans"
    recommendation = Column(String, nullable=True)

    def __repr__(self):
        return f"<PoolLevelInsightsWidget(id={self.id}, score={self.score})>"


class PoolLevelData(Base):
    __tablename__ = "pool_level_data"

    id = Column(Integer, primary_key=True, autoincrement=True)
    pool_number = Column(String, nullable=False)
    loan_number = Column(String, nullable=False)
    number_of_findings = Column(Integer, nullable=False, default=0)
    violation_severity = Column(String, nullable=True)
    loan_docs_completeness = Column(Float, nullable=True)  # percentage
    default_probability_score = Column(Float, nullable=True)

    def __repr__(self):
        return (
            f"<PoolLevelData(pool={self.pool_number}, "
            f"loan={self.loan_number}, findings={self.number_of_findings})>"
        )


class LoanLevelInsightsWidget(Base):
    __tablename__ = "loan_level_insights_widgets"

    id = Column(Integer, primary_key=True, autoincrement=True)
    qc_findings = Column(Float, nullable=False)
    epd_percent = Column(Float, nullable=False)
    score = Column(Float, nullable=False)
    watchlist_deficiency_categories = Column(String, nullable=True)
    recommendation = Column(String, nullable=True)

    def __repr__(self):
        return (
            f"<LoanLevelInsightsWidget(id={self.id}, "
            f"qc_findings={self.qc_findings}, score={self.score})>"
        )


class QCFindingDetailsLoanLevel(Base):
    __tablename__ = "qc_finding_details_loan_level"

    id = Column(Integer, primary_key=True, autoincrement=True)
    loan_number = Column(String, nullable=False)
    loan_amount = Column(Float, nullable=True)
    fico = Column(Float, nullable=True)
    interest_rate = Column(Float, nullable=True)
    loan_type = Column(String, nullable=True)
    occupancy = Column(String, nullable=True)
    funding_date = Column(String, nullable=True)
    loan_purpose = Column(String, nullable=True)
    loan_program = Column(String, nullable=True)
    ltv = Column(Float, nullable=True)

    def __repr__(self):
        return f"<QCFindingDetailsLoanLevel(loan={self.loan_number}, fico={self.fico})>"


class DeficienciesIdentified(Base):
    __tablename__ = "deficiencies_identified"

    id = Column(Integer, primary_key=True, autoincrement=True)
    loan_number = Column(String, nullable=False)
    deficiency_category = Column(String, nullable=True)
    sub_category = Column(String, nullable=True)
    deficiency_def = Column(String, nullable=True)
    finding_impact = Column(String, nullable=True)
    cure_status = Column(String, nullable=True)
    cured_reason = Column(String, nullable=True)

    def __repr__(self):
        return f"<DeficienciesIdentified(loan={self.loan_number}, category={self.deficiency_category})>"
