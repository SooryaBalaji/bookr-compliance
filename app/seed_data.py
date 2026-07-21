# app/seed_data.py
# Comprehensive compliance frameworks mapped to 2026 statutory requirements.

STATE_TASKS_MAP = {
    "Alabama": [
        {'key': 'al_bpt', 'num': 46, 'quarter': 'Q2', 'scope': 'Alabama', 'short': 'AL BPT Return',
         'title': 'Alabama Business Privilege Tax Return', 'due_type': 'fixed', 'due_month': 4, 'due_day': 15,
         'due_text': 'April 15', 'portal_name': 'AL MAT Portal', 'portal_url': 'https://myalabamataxes.alabama.gov/',
         'info': 'Annual privilege tax filing required for all entities.'}
    ],
    "Alaska": [
        {'key': 'ak_biennial', 'num': 47, 'quarter': 'Q1', 'scope': 'Alaska', 'short': 'AK Biennial Report',
         'title': 'Alaska Biennial Corporate / LLC Report', 'due_type': 'fixed', 'due_month': 1, 'due_day': 2,
         'due_text': 'January 2', 'portal_name': 'AK Corp Division',
         'portal_url': 'https://www.commerce.alaska.gov/cbp/main/',
         'info': 'Filed biennially based on odd/even year of formation.'}
    ],
    "Arizona": [
        {'key': 'az_ar', 'num': 48, 'quarter': 'ROLL', 'scope': 'Arizona', 'short': 'AZ Annual Report',
         'title': 'Arizona Corporation Annual Report', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
         'due_text': 'Anniversary Date', 'portal_name': 'AZ eCorp', 'portal_url': 'https://ecorp.azcc.gov/',
         'info': 'Required for Corporations. (AZ LLCs are exempt from state annual reports).'}
    ],
    "Arkansas": [
        {'key': 'ar_franchise', 'num': 49, 'quarter': 'Q2', 'scope': 'Arkansas', 'short': 'AR Franchise Tax',
         'title': 'Arkansas Annual Franchise Tax Report', 'due_type': 'fixed', 'due_month': 5, 'due_day': 1,
         'due_text': 'May 1', 'portal_name': 'AR SOS Portal', 'portal_url': 'https://www.sos.arkansas.gov/',
         'info': 'Annual franchise tax due for Corporations and LLCs.'}
    ],
    "California": [
        {'key': 'ca_si_200', 'num': 50, 'quarter': 'ROLL', 'scope': 'California', 'short': 'CA Statement of Info',
         'title': 'California Statement of Information (SI-550/LLC-12)', 'due_type': 'rolling', 'due_month': None,
         'due_day': None,
         'due_text': 'Anniversary Month', 'portal_name': 'bizfile Online',
         'portal_url': 'https://bizfileonline.sos.ca.gov/',
         'info': 'Annual (Corp) or Biennial (LLC) filing.'}
    ],
    "Colorado": [
        {'key': 'co_periodic', 'num': 51, 'quarter': 'ROLL', 'scope': 'Colorado', 'short': 'CO Periodic Report',
         'title': 'Colorado Periodic Report', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
         'due_text': 'End of 2nd Month After Anniversary Month', 'portal_name': 'CO SOS Business Portal',
         'portal_url': 'https://www.sos.state.co.us/',
         'info': 'Filing window runs from 2 months before the anniversary month through the end of the 2nd month after it (C.R.S. §7-90-501); not delinquent until that window closes.'}
    ],
    "Connecticut": [
        {'key': 'ct_ar', 'num': 52, 'quarter': 'Q1', 'scope': 'Connecticut', 'short': 'CT Annual Report',
         'title': 'Connecticut Annual Report', 'due_type': 'fixed', 'due_month': 3, 'due_day': 31,
         'due_text': 'March 31 (LLC/LP/LLP) — Corps file by end of anniversary month instead',
         'portal_name': 'CT CONCORD', 'portal_url': 'https://service.ct.gov/',
         'info': 'LLCs, LPs, and LLPs file by March 31. Stock and non-stock Corporations instead file by the last day of their anniversary month, not March 31.'}
    ],
    "Delaware": [
        {'key': 'de_fran_tax', 'num': 53, 'quarter': 'Q1', 'scope': 'Delaware', 'short': 'DE Franchise Tax',
         'title': 'Delaware Franchise Tax & Annual Report', 'due_type': 'fixed', 'due_month': 3, 'due_day': 1,
         'due_text': 'March 1 (Corp) / June 1 (LLC)', 'portal_name': 'DE eCorp',
         'portal_url': 'https://icis.corp.delaware.gov/ecorp/',
         'info': 'Mandatory for DE entities.'}
    ],
    "Florida": [
        {'key': 'fl_ar', 'num': 54, 'quarter': 'Q2', 'scope': 'Florida', 'short': 'FL Annual Report',
         'title': 'Florida Annual Report', 'due_type': 'fixed', 'due_month': 5, 'due_day': 1,
         'due_text': 'May 1', 'portal_name': 'Sunbiz', 'portal_url': 'https://corplaw.dos.state.fl.us/',
         'info': 'Substantial $400 penalty if filed after May 1.'}
    ],
    "Georgia": [
        {'key': 'ga_registration', 'num': 55, 'quarter': 'Q2', 'scope': 'Georgia', 'short': 'GA Annual Registration',
         'title': 'Georgia Annual Registration', 'due_type': 'fixed', 'due_month': 4, 'due_day': 1,
         'due_text': 'April 1', 'portal_name': 'GA eCorp', 'portal_url': 'https://ecorp.sos.ga.gov/',
         'info': 'Annual registration filing for active business entities.'}
    ],
    "Hawaii": [
        {'key': 'hi_ar', 'num': 56, 'quarter': 'ROLL', 'scope': 'Hawaii', 'short': 'HI Annual Report',
         'title': 'Hawaii Annual Report', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
         'due_text': 'Anniversary Quarter', 'portal_name': 'HI Business Express',
         'portal_url': 'https://hbe.ehawaii.gov/',
         'info': 'Due during the quarter of original registration.'}
    ],
    "Idaho": [
        {'key': 'id_ar', 'num': 57, 'quarter': 'ROLL', 'scope': 'Idaho', 'short': 'ID Annual Report',
         'title': 'Idaho Annual Report', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
         'due_text': 'Anniversary Month', 'portal_name': 'ID bizfile', 'portal_url': 'https://sosbiz.idaho.gov/',
         'info': 'No state filing fee, mandatory annual report.'}
    ],
    "Illinois": [
        {'key': 'il_ar', 'num': 58, 'quarter': 'ROLL', 'scope': 'Illinois', 'short': 'IL Annual Report',
         'title': 'Illinois Annual Report & Franchise Tax', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
         'due_text': 'Prior to Anniversary Month', 'portal_name': 'IL CyberDrive',
         'portal_url': 'https://www.ilsos.gov/',
         'info': 'Must be filed prior to the first day of anniversary month.'}
    ],
    "Indiana": [
        {'key': 'in_ber', 'num': 59, 'quarter': 'ROLL', 'scope': 'Indiana', 'short': 'IN Business Entity Report',
         'title': 'Indiana Business Entity Report', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
         'due_text': 'Biennial Anniversary Month', 'portal_name': 'INBiz', 'portal_url': 'https://inbiz.in.gov/',
         'info': 'Filed biennially in the anniversary month.'}
    ],
    "Iowa": [
        {'key': 'ia_biennial', 'num': 60, 'quarter': 'Q2', 'scope': 'Iowa', 'short': 'IA Biennial Report',
         'title': 'Iowa Biennial Report', 'due_type': 'fixed', 'due_month': 4, 'due_day': 1,
         'due_text': 'April 1', 'portal_name': 'IA Fast Track Filing', 'portal_url': 'https://filings.sos.iowa.gov/',
         'info': 'Even years for Corporations; Odd years for LLCs.'}
    ],
    "Kansas": [
        {'key': 'ks_ar', 'num': 61, 'quarter': 'Q2', 'scope': 'Kansas', 'short': 'KS Annual Report',
         'title': 'Kansas Annual / Biennial Report', 'due_type': 'fixed', 'due_month': 4, 'due_day': 15,
         'due_text': 'April 15', 'portal_name': 'KS KanFile', 'portal_url': 'https://www.kansas.gov/bess/',
         'info': 'Required for active business entities in Kansas.'}
    ],
    "Kentucky": [
        {'key': 'ky_ar', 'num': 62, 'quarter': 'Q2', 'scope': 'Kentucky', 'short': 'KY Annual Report',
         'title': 'Kentucky Annual Report', 'due_type': 'fixed', 'due_month': 6, 'due_day': 30,
         'due_text': 'June 30', 'portal_name': 'KY Online Services', 'portal_url': 'https://www.sos.ky.gov/',
         'info': 'Required annually by June 30.'}
    ],
    "Louisiana": [
        {'key': 'la_ar', 'num': 63, 'quarter': 'ROLL', 'scope': 'Louisiana', 'short': 'LA Annual Report',
         'title': 'Louisiana Annual Report', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
         'due_text': 'Anniversary Date', 'portal_name': 'geauxBIZ', 'portal_url': 'https://geauxbiz.sos.la.gov/',
         'info': 'Due annually on or before charter date.'}
    ],
    "Maine": [
        {'key': 'me_ar', 'num': 64, 'quarter': 'Q2', 'scope': 'Maine', 'short': 'ME Annual Report',
         'title': 'Maine Annual Report', 'due_type': 'fixed', 'due_month': 6, 'due_day': 1,
         'due_text': 'June 1', 'portal_name': 'ME Corporate Filing', 'portal_url': 'https://www.maine.gov/sos/',
         'info': 'Required for all Maine active registered entities.'}
    ],
    "Maryland": [
        {'key': 'md_f1', 'num': 65, 'quarter': 'Q2', 'scope': 'Maryland', 'short': 'MD Form 1 AR',
         'title': 'Maryland Annual Report & Personal Property Return', 'due_type': 'fixed', 'due_month': 4,
         'due_day': 15,
         'due_text': 'April 15', 'portal_name': 'Maryland Business Express',
         'portal_url': 'https://egov.maryland.gov/businessexpress',
         'info': 'Mandatory personal property tax and annual report.'}
    ],
    "Massachusetts": [
        {'key': 'ma_ar', 'num': 66, 'quarter': 'ROLL', 'scope': 'Massachusetts', 'short': 'MA Annual Report',
         'title': 'Massachusetts Annual Report', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
         'due_text': 'Anniversary Date (LLC) / 2.5 mo FY Close (Corp)', 'portal_name': 'MA SOC Portal',
         'portal_url': 'https://www.sec.state.ma.us/cor/',
         'info': 'Annual corporate report requirement.'}
    ],
    "Michigan": [
        {'key': 'mi_ar', 'num': 67, 'quarter': 'Q2', 'scope': 'Michigan', 'short': 'MI Annual Statement',
         'title': 'Michigan Annual Report / Statement', 'due_type': 'fixed', 'due_month': 5, 'due_day': 15,
         'due_text': 'May 15 (Corp) / Feb 15 (LLC)', 'portal_name': 'MI LARA Portal',
         'portal_url': 'https://cora.lara.michigan.gov/',
         'info': 'Annual filing with Department of Licensing and Regulatory Affairs.'}
    ],
    "Minnesota": [
        {'key': 'mn_renewal', 'num': 68, 'quarter': 'Q4', 'scope': 'Minnesota', 'short': 'MN Annual Renewal',
         'title': 'Minnesota Annual Renewal', 'due_type': 'fixed', 'due_month': 12, 'due_day': 31,
         'due_text': 'December 31', 'portal_name': 'MN MBLS Portal',
         'portal_url': 'https://mblsportal.sos.state.mn.us/',
         'info': 'Required annually by December 31.'}
    ],
    "Mississippi": [
        {'key': 'ms_ar', 'num': 69, 'quarter': 'Q2', 'scope': 'Mississippi', 'short': 'MS Annual Report',
         'title': 'Mississippi Annual Report', 'due_type': 'fixed', 'due_month': 4, 'due_day': 15,
         'due_text': 'April 15', 'portal_name': 'MS SOS Portal', 'portal_url': 'https://corp.sos.ms.gov/',
         'info': 'Mandatory annual report filing.'}
    ],
    "Missouri": [
        {'key': 'mo_ar', 'num': 70, 'quarter': 'ROLL', 'scope': 'Missouri', 'short': 'MO Annual Report',
         'title': 'Missouri Corporation Annual Report', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
         'due_text': 'End of 3rd Month Post-Anniversary', 'portal_name': 'MO Online Business Services',
         'portal_url': 'https://bsd.sos.mo.gov/',
         'info': 'Corporations only (MO LLCs are exempt).'}
    ],
    "Montana": [
        {'key': 'mt_ar', 'num': 71, 'quarter': 'Q2', 'scope': 'Montana', 'short': 'MT Annual Report',
         'title': 'Montana Annual Report', 'due_type': 'fixed', 'due_month': 4, 'due_day': 15,
         'due_text': 'April 15', 'portal_name': 'MT SIMS Portal', 'portal_url': 'https://biz.sosmt.gov/',
         'info': 'Required for active business entities.'}
    ],
    "Nebraska": [
        {'key': 'ne_biennial', 'num': 72, 'quarter': 'Q1', 'scope': 'Nebraska', 'short': 'NE Biennial Report',
         'title': 'Nebraska Biennial Report & Occupation Tax', 'due_type': 'fixed', 'due_month': 3, 'due_day': 1,
         'due_text': 'March 1 (Even Yrs Corp) / April 1 (Odd Yrs LLC)', 'portal_name': 'NE Corporate Portal',
         'portal_url': 'https://www.nebraska.gov/sos/corp/',
         'info': 'Occupation tax report.'}
    ],
    "Nevada": [
        {'key': 'nv_annual_list', 'num': 73, 'quarter': 'ROLL', 'scope': 'Nevada', 'short': 'NV Annual List',
         'title': 'Nevada Annual List of Officers/Managers & State License', 'due_type': 'rolling', 'due_month': None,
         'due_day': None,
         'due_text': 'Last Day of Anniversary Month', 'portal_name': 'SilverFlume',
         'portal_url': 'https://www.nvsilverflume.gov/',
         'info': 'Annual List filing fee + state business license fee.'}
    ],
    "New Hampshire": [
        {'key': 'nh_ar', 'num': 74, 'quarter': 'Q2', 'scope': 'New Hampshire', 'short': 'NH Annual Report',
         'title': 'New Hampshire Annual Report', 'due_type': 'fixed', 'due_month': 4, 'due_day': 1,
         'due_text': 'April 1', 'portal_name': 'NH QuickStart', 'portal_url': 'https://quickstart.sos.nh.gov/',
         'info': 'Mandatory corporate filing.'}
    ],
    "New Jersey": [
        {'key': 'nj_ar', 'num': 75, 'quarter': 'ROLL', 'scope': 'New Jersey', 'short': 'NJ Annual Report',
         'title': 'New Jersey Annual Report', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
         'due_text': 'End of Month Prior to Anniversary', 'portal_name': 'NJ Premier Business Services',
         'portal_url': 'https://www.njportal.com/dor/annualreports',
         'info': 'Required for all active NJ domestic/foreign qualified entities.'}
    ],
    "New Mexico": [
        {'key': 'nm_biennial', 'num': 76, 'quarter': 'Q2', 'scope': 'New Mexico', 'short': 'NM Corporate Biennial',
         'title': 'New Mexico Corporate Biennial Report', 'due_type': 'fixed', 'due_month': 4, 'due_day': 15,
         'due_text': '15th Day of 4th Month Post-FY', 'portal_name': 'NM SOS Portal',
         'portal_url': 'https://portal.sos.state.nm.us/',
         'info': 'Corporations only (NM LLCs are exempt from filing).'}
    ],
    "New York": [
        {'key': 'ny_biennial', 'num': 77, 'quarter': 'ROLL', 'scope': 'New York', 'short': 'NY Biennial Statement',
         'title': 'New York Biennial Statement', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
         'due_text': 'Anniversary Month', 'portal_name': 'NY Dept of State Portal', 'portal_url': 'https://dos.ny.gov/',
         'info': 'Filed every 2 years during anniversary month.'}
    ],
    "North Carolina": [
        {'key': 'nc_ar', 'num': 78, 'quarter': 'Q2', 'scope': 'North Carolina', 'short': 'NC Annual Report',
         'title': 'North Carolina Annual Report', 'due_type': 'fixed', 'due_month': 4, 'due_day': 15,
         'due_text': 'April 15', 'portal_name': 'NC SOS Portal', 'portal_url': 'https://www.sosnc.gov/',
         'info': 'Annual report required for LLCs and Corporations.'}
    ],
    "North Dakota": [
        {'key': 'nd_ar', 'num': 79, 'quarter': 'Q3', 'scope': 'North Dakota', 'short': 'ND Annual Report',
         'title': 'North Dakota Annual Report', 'due_type': 'fixed', 'due_month': 8, 'due_day': 1,
         'due_text': 'August 1 (Corp) / Nov 15 (LLC)', 'portal_name': 'ND FirstStop',
         'portal_url': 'https://firststop.sos.nd.gov/',
         'info': 'State statutory report.'}
    ],
    "Ohio": [
        {'key': 'oh_notice', 'num': 80, 'quarter': 'ROLL', 'scope': 'Ohio',
         'short': 'OH Statement of Continued Existence',
         'title': 'Ohio Statement of Continued Existence', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
         'due_text': 'Every 5 Years', 'portal_name': 'OH Business Central', 'portal_url': 'https://bsd.ohiosos.gov/',
         'info': 'Ohio does not require general annual reports, only 5-year renewals for specific entities.'}
    ],
    "Oklahoma": [
        {'key': 'ok_certificate', 'num': 81, 'quarter': 'ROLL', 'scope': 'Oklahoma', 'short': 'OK Annual Certificate',
         'title': 'Oklahoma Annual Certificate / Franchise Tax', 'due_type': 'rolling', 'due_month': None,
         'due_day': None,
         'due_text': 'Anniversary Date (LLC) / July 1 (Corp)', 'portal_name': 'OK SOS Filing',
         'portal_url': 'https://www.sos.ok.gov/',
         'info': 'Annual business certificate maintenance.'}
    ],
    "Oregon": [
        {'key': 'or_ar', 'num': 82, 'quarter': 'ROLL', 'scope': 'Oregon', 'short': 'OR Annual Report',
         'title': 'Oregon Annual Report', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
         'due_text': 'Anniversary Date', 'portal_name': 'OR Business Registry',
         'portal_url': 'https://sos.oregon.gov/business',
         'info': 'Annual report filing requirement.'}
    ],
    "Pennsylvania": [
        {'key': 'pa_ar', 'num': 83, 'quarter': 'Q2', 'scope': 'Pennsylvania', 'short': 'PA Annual Report',
         'title': 'Pennsylvania Annual Report', 'due_type': 'fixed', 'due_month': 6, 'due_day': 30,
         'due_text': 'June 30 (Corp) / Sept 30 (LLC)', 'portal_name': 'PA Business One-Stop Hub',
         'portal_url': 'https://hub.business.pa.gov/',
         'info': 'New annual report requirement effective in PA.'}
    ],
    "Rhode Island": [
        {'key': 'ri_ar', 'num': 84, 'quarter': 'Q2', 'scope': 'Rhode Island', 'short': 'RI Annual Report',
         'title': 'Rhode Island Annual Report', 'due_type': 'fixed', 'due_month': 5, 'due_day': 1,
         'due_text': 'May 1', 'portal_name': 'RI Corporate Portal', 'portal_url': 'https://bizportal.sos.ri.gov/',
         'info': 'Mandatory corporate filing.'}
    ],
    "South Carolina": [
        {'key': 'sc_ar', 'num': 85, 'quarter': 'Q2', 'scope': 'South Carolina', 'short': 'SC Annual Report',
         'title': 'South Carolina Corporate Annual Report (CL-1)', 'due_type': 'fixed', 'due_month': 4, 'due_day': 15,
         'due_text': 'April 15', 'portal_name': 'SC DOR Portal', 'portal_url': 'https://mydorway.sctax.org/',
         'info': 'Filed alongside state tax returns for Corporations (SC LLCs are exempt).'}
    ],
    "South Dakota": [
        {'key': 'sd_ar', 'num': 86, 'quarter': 'ROLL', 'scope': 'South Dakota', 'short': 'SD Annual Report',
         'title': 'South Dakota Annual Report', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
         'due_text': 'First Day of Anniversary Month', 'portal_name': 'SD Corporate Portal',
         'portal_url': 'https://sdsos.gov/',
         'info': 'Annual filing requirement.'}
    ],
    "Tennessee": [
        {'key': 'tn_ar', 'num': 87, 'quarter': 'Q2', 'scope': 'Tennessee', 'short': 'TN Annual Report',
         'title': 'Tennessee Annual Report', 'due_type': 'fixed', 'due_month': 4, 'due_day': 1,
         'due_text': '1st Day of 4th Month Post-FY', 'portal_name': 'TN Business Services',
         'portal_url': 'https://tnbear.tn.gov/',
         'info': 'State annual report.'}
    ],
    "Texas": [
        {'key': 'tx_franchise', 'num': 88, 'quarter': 'Q2', 'scope': 'Texas', 'short': 'TX Franchise Tax & PIR',
         'title': 'Texas Franchise Tax & Public Information Report', 'due_type': 'fixed', 'due_month': 5, 'due_day': 15,
         'due_text': 'May 15', 'portal_name': 'TX Webfile',
         'portal_url': 'https://comptroller.texas.gov/taxes/franchise/',
         'info': 'Mandatory PIR filing required even if no franchise tax is owed.'}
    ],
    "Utah": [
        {'key': 'ut_renewal', 'num': 89, 'quarter': 'ROLL', 'scope': 'Utah', 'short': 'UT Annual Renewal',
         'title': 'Utah Annual Business Renewal / Report', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
         'due_text': 'Anniversary Month', 'portal_name': 'UT OneStop Business Registration',
         'portal_url': 'https://corporations.utah.gov/',
         'info': 'Annual renewal requirement.'}
    ],
    "Vermont": [
        {'key': 'vt_ar', 'num': 90, 'quarter': 'Q1', 'scope': 'Vermont', 'short': 'VT Annual Report',
         'title': 'Vermont Annual Report', 'due_type': 'fixed', 'due_month': 3, 'due_day': 31,
         'due_text': 'March 31 (LLC) — Corps file within 2.5 months of fiscal year close instead',
         'portal_name': 'VT Online Services', 'portal_url': 'https://bizfilings.vermont.gov/',
         'info': "LLCs file within 3 months of fiscal year close (March 31 for a calendar year). Corporations file within 2.5 months instead (~March 16 for a calendar year), per 11 V.S.A. Section 16.22."}
    ],
    "Virginia": [
        {'key': 'va_ar', 'num': 91, 'quarter': 'ROLL', 'scope': 'Virginia', 'short': 'VA Annual Registration',
         'title': 'Virginia Annual Report & Registration Fee', 'due_type': 'rolling', 'due_month': None,
         'due_day': None,
         'due_text': 'Last Day of Anniversary Month', 'portal_name': 'VA CIS Portal',
         'portal_url': 'https://cis.scc.virginia.gov/',
         'info': 'State registration renewal.'}
    ],
    "Washington": [
        {'key': 'wa_ar', 'num': 92, 'quarter': 'ROLL', 'scope': 'Washington', 'short': 'WA Annual Report',
         'title': 'Washington Annual Report', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
         'due_text': 'Last Day of Anniversary Month', 'portal_name': 'WA CCFS Portal',
         'portal_url': 'https://ccfs.sos.wa.gov/',
         'info': 'Mandatory corporate renewal.'}
    ],
    "West Virginia": [
        {'key': 'wv_ar', 'num': 93, 'quarter': 'Q2', 'scope': 'West Virginia', 'short': 'WV Annual Report',
         'title': 'West Virginia Annual Report', 'due_type': 'fixed', 'due_month': 6, 'due_day': 30,
         'due_text': 'June 30', 'portal_name': 'WV One Stop Portal', 'portal_url': 'https://extranet.wvsos.gov/',
         'info': 'State annual report.'}
    ],
    "Wisconsin": [
        {'key': 'wi_ar', 'num': 94, 'quarter': 'ROLL', 'scope': 'Wisconsin', 'short': 'WI Annual Report',
         'title': 'Wisconsin Annual Report', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
         'due_text': 'End of Anniversary Quarter', 'portal_name': 'WI DFI Portal',
         'portal_url': 'https://www.wdfi.org/',
         'info': 'Mandatory corporate filing.'}
    ],
    "Wyoming": [
        {'key': 'wy_ar', 'num': 95, 'quarter': 'ROLL', 'scope': 'Wyoming', 'short': 'WY Annual Report',
         'title': 'Wyoming Annual Report & Tax', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
         'due_text': 'First Day of Anniversary Month', 'portal_name': 'WY Business Filing System',
         'portal_url': 'https://wyobiz.wyo.gov/',
         'info': 'Minimum tax based on assets in Wyoming.'}
    ],
    "District of Columbia": [
        {'key': 'dc_biennial', 'num': 96, 'quarter': 'Q2', 'scope': 'District of Columbia',
         'short': 'DC Biennial Report',
         'title': 'District of Columbia Biennial Report (BRA-25)', 'due_type': 'fixed', 'due_month': 4, 'due_day': 1,
         'due_text': 'April 1', 'portal_name': 'DC CorpOnline', 'portal_url': 'https://corponline.dlcp.dc.gov/',
         'info': 'Filed every two years on April 1.'}
    ]
}

CORE_TASKS = [
    # January
    {'key': 'bk_941q4', 'num': 1, 'quarter': 'Q1', 'scope': 'Federal', 'short': '941 Q4',
     'title': 'Employer’s Quarterly Federal Tax Return - Q4', 'due_type': 'fixed', 'due_month': 1, 'due_day': 31,
     'due_text': 'January 31', 'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/',
     'info': 'Reconciles federal income tax withholding for Q4.'},
    {'key': 'bk_940', 'num': 2, 'quarter': 'Q1', 'scope': 'Federal', 'short': '940 FUTA',
     'title': 'Federal Annual Unemployment Tax', 'due_type': 'fixed', 'due_month': 1, 'due_day': 31,
     'due_text': 'January 31', 'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/',
     'info': 'Assesses FUTA liability on the first $7,000 paid to each W-2 employee.'},
    {'key': 'bk_1099', 'num': 3, 'quarter': 'Q1', 'scope': 'Federal', 'short': '1099-NEC',
     'title': 'Form 1099-NEC Filing & Distribution', 'due_type': 'fixed', 'due_month': 1, 'due_day': 31,
     'due_text': 'January 31', 'portal_name': 'IRS FIRE', 'portal_url': 'https://fire.irs.gov/',
     'info': 'Required for unincorporated contractors paid $600+.'},
    {'key': 'bk_w2', 'num': 4, 'quarter': 'Q1', 'scope': 'Federal', 'short': 'W-2 / W-3',
     'title': 'Wage and Tax Statements', 'due_type': 'fixed', 'due_month': 1, 'due_day': 31, 'due_text': 'January 31',
     'portal_name': 'SSA BSO', 'portal_url': 'https://www.ssa.gov/bso/', 'info': 'Transmittal of employee earnings.'},
    {'key': 'bk_de9_4', 'num': 5, 'quarter': 'Q1', 'scope': 'California', 'short': 'DE 9/9C Q4',
     'title': 'CA EDD Quarterly Payroll Returns - Q4', 'due_type': 'fixed', 'due_month': 1, 'due_day': 31,
     'due_text': 'January 31', 'portal_name': 'CA EDD', 'portal_url': 'https://edd.ca.gov/e-Services_for_Business.htm',
     'info': 'State payroll tax reconciliation.'},

    # March
    {'key': 'bk_de_fran', 'num': 6, 'quarter': 'Q1', 'scope': 'Delaware', 'short': 'DE Franchise Tax',
     'title': 'Delaware Annual Franchise Tax & Report', 'due_type': 'fixed', 'due_month': 3, 'due_day': 1,
     'due_text': 'March 1', 'portal_name': 'DE eCorp', 'portal_url': 'https://icis.corp.delaware.gov/ecorp/',
     'info': 'Mandatory for all DE C-Corps. Requires $50 filing fee + minimum tax.'},
    {'key': 'bk_de_esch', 'num': 7, 'quarter': 'Q1', 'scope': 'Delaware', 'short': 'DE Escheatment',
     'title': 'DE Unclaimed Property Report', 'due_type': 'fixed', 'due_month': 3, 'due_day': 1, 'due_text': 'March 1',
     'portal_name': 'DE Dept of Finance', 'portal_url': 'https://unclaimedproperty.delaware.gov/',
     'info': 'Filing required even if there is no unclaimed property (Negative Report).'},
    {'key': 'bk_osha', 'num': 8, 'quarter': 'Q1', 'scope': 'Federal', 'short': 'OSHA 300A',
     'title': 'Cal/OSHA Form 300A Summary Submission', 'due_type': 'fixed', 'due_month': 3, 'due_day': 2,
     'due_text': 'March 2', 'portal_name': 'OSHA ITA', 'portal_url': 'https://www.osha.gov/injuryreporting/',
     'info': 'Electronic submission of work-related injuries/illnesses summary.'},
    {'key': 'bk_aca', 'num': 9, 'quarter': 'Q1', 'scope': 'Federal', 'short': 'ACA 1094/1095-C',
     'title': 'Affordable Care Act Employer Reporting', 'due_type': 'fixed', 'due_month': 3, 'due_day': 31,
     'due_text': 'March 31', 'portal_name': 'IRS AIR', 'portal_url': 'https://www.irs.gov/e-file-providers/air',
     'info': 'Electronic filing deadline. Required for Applicable Large Employers (50+ FTEs).'},

    # April
    {'key': 'bk_571l', 'num': 10, 'quarter': 'Q2', 'scope': 'California', 'short': 'Form 571-L',
     'title': 'Business Property Statement', 'due_type': 'fixed', 'due_month': 4, 'due_day': 1, 'due_text': 'April 1',
     'portal_name': 'County Assessor', 'portal_url': 'https://www.calassessor.org/',
     'info': 'Required if unsecured business property exceeds $100k.'},
    {'key': 'bk_1120', 'num': 11, 'quarter': 'Q2', 'scope': 'Federal', 'short': 'Form 1120',
     'title': 'U.S. Corporation Income Tax Return', 'due_type': 'fixed', 'due_month': 4, 'due_day': 15,
     'due_text': 'April 15', 'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/',
     'info': 'Core federal income tax return. Can be extended to Oct 15 via Form 7004.'},
    {'key': 'bk_1120w_1', 'num': 12, 'quarter': 'Q2', 'scope': 'Federal', 'short': '1120-W Q1',
     'title': 'Fed Est. Tax - Installment 1', 'due_type': 'fixed', 'due_month': 4, 'due_day': 15,
     'due_text': 'April 15', 'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/',
     'info': 'Federal estimated tax payment.'},
    {'key': 'bk_ftb100', 'num': 13, 'quarter': 'Q2', 'scope': 'California', 'short': 'FTB Form 100',
     'title': 'CA Corporation Franchise & Income Tax Return', 'due_type': 'fixed', 'due_month': 4, 'due_day': 15,
     'due_text': 'April 15', 'portal_name': 'FTB Web Pay', 'portal_url': 'https://www.ftb.ca.gov/pay/',
     'info': 'Includes CA’s 8.84% corporate rate and the $800 minimum tax.'},
    {'key': 'bk_ca_100es1', 'num': 14, 'quarter': 'Q2', 'scope': 'California', 'short': '100-ES Q1',
     'title': 'CA Est. Tax - Installment 1 (30%)', 'due_type': 'fixed', 'due_month': 4, 'due_day': 15,
     'due_text': 'April 15', 'portal_name': 'FTB Web Pay', 'portal_url': 'https://www.ftb.ca.gov/pay/',
     'info': 'First state estimated payment.'},
    {'key': 'bk_941q1', 'num': 15, 'quarter': 'Q2', 'scope': 'Federal', 'short': '941 Q1',
     'title': 'Employer’s Quarterly Federal Tax Return - Q1', 'due_type': 'fixed', 'due_month': 4, 'due_day': 30,
     'due_text': 'April 30', 'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/',
     'info': 'Reconciles federal income tax withholding for Q1.'},
    {'key': 'bk_de9_1', 'num': 16, 'quarter': 'Q2', 'scope': 'California', 'short': 'DE 9/9C Q1',
     'title': 'CA EDD Quarterly Payroll Returns - Q1', 'due_type': 'fixed', 'due_month': 4, 'due_day': 30,
     'due_text': 'April 30', 'portal_name': 'CA EDD', 'portal_url': 'https://edd.ca.gov/e-Services_for_Business.htm',
     'info': 'State payroll tax reconciliation.'},

    # May
    {'key': 'bk_ca_paydata', 'num': 17, 'quarter': 'Q2', 'scope': 'California', 'short': 'CA Pay Data',
     'title': 'CA Pay Data Report', 'due_type': 'fixed', 'due_month': 5, 'due_day': 13, 'due_text': 'May (2nd Wed)',
     'portal_name': 'CRD Portal', 'portal_url': 'https://calcivilrights.ca.gov/paydatareporting/',
     'info': 'Required if crossing 100-employee threshold.'},

    # June
    {'key': 'bk_1120w_2', 'num': 18, 'quarter': 'Q2', 'scope': 'Federal', 'short': '1120-W Q2',
     'title': 'Fed Est. Tax - Installment 2', 'due_type': 'fixed', 'due_month': 6, 'due_day': 15, 'due_text': 'June 15',
     'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/', 'info': 'Federal estimated tax payment.'},
    {'key': 'bk_ca_100es2', 'num': 19, 'quarter': 'Q2', 'scope': 'California', 'short': '100-ES Q2',
     'title': 'CA Est. Tax - Installment 2 (40%)', 'due_type': 'fixed', 'due_month': 6, 'due_day': 15,
     'due_text': 'June 15', 'portal_name': 'FTB Web Pay', 'portal_url': 'https://www.ftb.ca.gov/pay/',
     'info': 'Second state estimated payment.'},

    # July
    {'key': 'bk_941q2', 'num': 20, 'quarter': 'Q3', 'scope': 'Federal', 'short': '941 Q2',
     'title': 'Employer’s Quarterly Federal Tax Return - Q2', 'due_type': 'fixed', 'due_month': 7, 'due_day': 31,
     'due_text': 'July 31', 'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/',
     'info': 'Reconciles federal income tax withholding for Q2.'},
    {'key': 'bk_de9_2', 'num': 21, 'quarter': 'Q3', 'scope': 'California', 'short': 'DE 9/9C Q2',
     'title': 'CA EDD Quarterly Payroll Returns - Q2', 'due_type': 'fixed', 'due_month': 7, 'due_day': 31,
     'due_text': 'July 31', 'portal_name': 'CA EDD', 'portal_url': 'https://edd.ca.gov/e-Services_for_Business.htm',
     'info': 'State payroll tax reconciliation.'},
    {'key': 'bk_5500', 'num': 22, 'quarter': 'Q3', 'scope': 'Federal', 'short': 'Form 5500',
     'title': 'Annual Return/Report of Employee Benefit Plan', 'due_type': 'fixed', 'due_month': 7, 'due_day': 31,
     'due_text': 'July 31', 'portal_name': 'EFAST2', 'portal_url': 'https://www.efast.dol.gov/',
     'info': 'Required for 401(k) plans and health/welfare plans with 100+ participants.'},

    {'key': 'bk_si550', 'num': 23, 'quarter': 'ROLL', 'scope': 'California', 'short': 'Form SI-550',
     'title': 'California Statement of Information', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
     'due_text': 'Last Day of Anniversary Month', 'portal_name': 'bizfile Online', 'portal_url': 'https://bizfileonline.sos.ca.gov/',
     'info': 'File in the anniversary month of incorporation.'},

    # September
    {'key': 'bk_1120w_3', 'num': 24, 'quarter': 'Q3', 'scope': 'Federal', 'short': '1120-W Q3',
     'title': 'Fed Est. Tax - Installment 3', 'due_type': 'fixed', 'due_month': 9, 'due_day': 15,
     'due_text': 'September 15', 'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/',
     'info': 'Federal estimated tax payment.'},
    {'key': 'bk_ca_100es3', 'num': 25, 'quarter': 'Q3', 'scope': 'California', 'short': '100-ES Q3',
     'title': 'CA Est. Tax - Installment 3 (0%)', 'due_type': 'fixed', 'due_month': 9, 'due_day': 15,
     'due_text': 'September 15', 'portal_name': 'FTB Web Pay', 'portal_url': 'https://www.ftb.ca.gov/pay/',
     'info': 'Third state estimated payment.'},

    # October
    {'key': 'bk_941q3', 'num': 26, 'quarter': 'Q4', 'scope': 'Federal', 'short': '941 Q3',
     'title': 'Employer’s Quarterly Federal Tax Return - Q3', 'due_type': 'fixed', 'due_month': 10, 'due_day': 31,
     'due_text': 'October 31', 'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/',
     'info': 'Reconciles federal income tax withholding for Q3.'},
    {'key': 'bk_de9_3', 'num': 27, 'quarter': 'Q4', 'scope': 'California', 'short': 'DE 9/9C Q3',
     'title': 'CA EDD Quarterly Payroll Returns - Q3', 'due_type': 'fixed', 'due_month': 10, 'due_day': 31,
     'due_text': 'October 31', 'portal_name': 'CA EDD', 'portal_url': 'https://edd.ca.gov/e-Services_for_Business.htm',
     'info': 'State payroll tax reconciliation.'},

    # December
    {'key': 'bk_1120w_4', 'num': 28, 'quarter': 'Q4', 'scope': 'Federal', 'short': '1120-W Q4',
     'title': 'Fed Est. Tax - Installment 4', 'due_type': 'fixed', 'due_month': 12, 'due_day': 15,
     'due_text': 'December 15', 'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/',
     'info': 'Federal estimated tax payment.'},
    {'key': 'bk_ca_100es4', 'num': 29, 'quarter': 'Q4', 'scope': 'California', 'short': '100-ES Q4',
     'title': 'CA Est. Tax - Installment 4 (30%)', 'due_type': 'fixed', 'due_month': 12, 'due_day': 15,
     'due_text': 'December 15', 'portal_name': 'FTB Web Pay', 'portal_url': 'https://www.ftb.ca.gov/pay/',
     'info': 'Final state estimated payment.'},

    # Rolling / Anniversary Deadlines
    {'key': 'bk_eeo1', 'num': 30, 'quarter': 'ROLL', 'scope': 'Federal', 'short': 'EEO-1 Report',
     'title': 'EEO-1 Component 1 Data Collection', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
     'due_text': 'Typically Fall (Check EEOC)', 'portal_name': 'EEOC Portal', 'portal_url': 'https://eeocdata.org/',
     'info': 'Demographic workforce data required if crossing the 100-employee threshold.'},
    {'key': 'bk_boi', 'num': 31, 'quarter': 'ROLL', 'scope': 'Federal', 'short': 'FinCEN BOI',
     'title': 'Beneficial Ownership Information Update', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
     'due_text': 'Exempt for U.S.-domestic entities (as of 2025)', 'portal_name': 'FinCEN E-Filing',
     'portal_url': 'https://boiefiling.fincen.gov/',
     'info': "As of FinCEN's March 2025 interim final rule, all entities formed in the U.S. (and their beneficial owners) are exempt from BOI reporting — only foreign companies registered to do business in the U.S. must still file. Monitor FinCEN.gov for changes to this exemption."},
    {'key': 'bk_agent', 'num': 32, 'quarter': 'ROLL', 'scope': 'Delaware', 'short': 'Registered Agent',
     'title': 'Registered Agent Annual Renewal', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
     'due_text': 'Annually', 'portal_name': 'Vcorp Portal', 'portal_url': 'https://www.vcorpservices.com/',
     'info': 'Maintains legal good standing in the state of formation.'},
    {'key': 'bk_ca_newhire', 'num': 33, 'quarter': 'ROLL', 'scope': 'California', 'short': 'DE 34',
     'title': 'CA EDD Report of New Employee(s)', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
     'due_text': 'Within 20 days of hire', 'portal_name': 'CA EDD e-Services',
     'portal_url': 'https://edd.ca.gov/e-Services_for_Business.htm',
     'info': 'Mandatory onboarding reporting.'},
    {'key': 'bk_ca_ic', 'num': 34, 'quarter': 'ROLL', 'scope': 'California', 'short': 'DE 542',
     'title': 'CA EDD Report of Independent Contractors', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
     'due_text': 'Within 20 days of $600+ payment', 'portal_name': 'CA EDD e-Services',
     'portal_url': 'https://edd.ca.gov/e-Services_for_Business.htm',
     'info': 'Mandatory 1099 onboarding reporting.'},
    {'key': 'bk_local', 'num': 35, 'quarter': 'ROLL', 'scope': 'Local', 'short': 'Local License',
     'title': 'Municipal Business Tax Certificate', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
     'due_text': 'Annually', 'portal_name': 'City Gov', 'portal_url': 'https://www.walnut-creek.org/',
     'info': 'Walnut Creek local business license renewal.'},
    {'key': 'bk_minutes', 'num': 36, 'quarter': 'ROLL', 'scope': 'Internal', 'short': 'Corp Minutes',
     'title': 'Annual Board of Directors & Shareholder Minutes', 'due_type': 'rolling', 'due_month': None,
     'due_day': None, 'due_text': 'Annually', 'portal_name': 'Internal', 'portal_url': '#',
     'info': 'Execute Unanimous Written Consents to maintain the corporate veil.'},
    {'key': 'bk_coterie', 'num': 37, 'quarter': 'ROLL', 'scope': 'Insurance', 'short': 'Prof. Liab.',
     'title': 'Professional Liability (E&O) Insurance Renewal', 'due_type': 'rolling', 'due_month': None,
     'due_day': None, 'due_text': 'Annually', 'portal_name': 'Broker', 'portal_url': '#',
     'info': 'Covers errors, omissions, and professional negligence.'},
    {'key': 'bk_gl', 'num': 38, 'quarter': 'ROLL', 'scope': 'Insurance', 'short': 'Gen. Liab.',
     'title': 'General Liability Insurance Renewal', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
     'due_text': 'Annually', 'portal_name': 'Broker', 'portal_url': '#',
     'info': 'Covers physical premise injuries and property damage.'},
    {'key': 'bk_wc', 'num': 39, 'quarter': 'ROLL', 'scope': 'Insurance', 'short': 'Workers Comp',
     'title': 'Workers Compensation Insurance Renewal', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
     'due_text': 'Annually', 'portal_name': 'Broker', 'portal_url': '#',
     'info': 'Statutory requirement in CA for any W-2 employees.'},
    {'key': 'bk_cyber', 'num': 40, 'quarter': 'ROLL', 'scope': 'Insurance', 'short': 'Cyber Liab.',
     'title': 'Cyber Liability Insurance Renewal', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
     'due_text': 'Annually', 'portal_name': 'Broker', 'portal_url': '#',
     'info': 'Covers data breaches and SaaS infrastructure vulnerabilities.'},

    # Restored Operational & Security Tasks
    {'key': 'bk_idmsosca', 'num': 41, 'quarter': 'ROLL', 'scope': 'California', 'short': 'CA SoS IDM',
     'title': 'CA Secretary of State Identity Management Portal Access', 'due_type': 'rolling', 'due_month': None,
     'due_day': None,
     'due_text': 'Continuous account management.', 'portal_name': 'idm.sos.ca.gov',
     'portal_url': 'https://idm.sos.ca.gov/signin/register',
     'info': 'Master CA SoS Identity Management credential system registration.'},

    {'key': 'bk_everify', 'num': 42, 'quarter': 'ROLL', 'scope': 'Federal', 'short': 'E-Verify USCIS',
     'title': 'E-Verify USCIS New Hire Verification Enrollment Protocol', 'due_type': 'rolling', 'due_month': None,
     'due_day': None,
     'due_text': 'Mandated for compliance upon onboarding new individuals.', 'portal_name': 'idp.uscis.gov',
     'portal_url': 'https://secure.login.gov/',
     'info': 'Workforce alignment tracking infrastructure configuration.'},

    {'key': 'bk_eftpsgov', 'num': 43, 'quarter': 'ROLL', 'scope': 'Federal', 'short': 'EFTPS Portal',
     'title': 'Federal Tax Portal Access and PIN Security Profile', 'due_type': 'rolling', 'due_month': None,
     'due_day': None,
     'due_text': 'Continuous account management.', 'portal_name': 'www.eftps.gov',
     'portal_url': 'https://secure.login.gov/',
     'info': 'IRS Federal Tax Payment Portal engine setup.'},

    {'key': 'bk_sterling', 'num': 44, 'quarter': 'ROLL', 'scope': 'Federal', 'short': 'Sterling HSA POP',
     'title': 'Sterling HSA Premium Only Plan Corporate Compliance Check', 'due_type': 'rolling', 'due_month': None,
     'due_day': None,
     'due_text': 'Continuous operational window monitoring status.', 'portal_name': 'Sterling HSA Engine',
     'portal_url': 'https://www.sterlinghsa.com/Accounts/Login/',
     'info': 'Premium Only Plan alignment checks mandated under IRS section code variables.'},

    {'key': 'bk_anthem', 'num': 45, 'quarter': 'ROLL', 'scope': 'Insurance', 'short': 'Anthem Portal',
     'title': 'Anthem Employer Health Insurance Premium Portal Management', 'due_type': 'rolling', 'due_month': None,
     'due_day': None,
     'due_text': 'Monthly accounting pipeline reconciliations.', 'portal_name': 'Anthem Employer Center',
     'portal_url': 'https://employer.anthem.com/eea/public/login',
     'info': 'Core operational workspace hub for tracking state group health enrollment variables.'}
]

CA_FOR_PROFIT_TASKS = [
    # January
    {'key': 'ca_c_941_4', 'num': 1, 'quarter': 'Q1', 'scope': 'Federal', 'short': '941 Q4',
     'title': 'Federal Payroll Tax - Q4', 'due_type': 'fixed', 'due_month': 1, 'due_day': 31, 'due_text': 'January 31',
     'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/', 'info': 'Quarterly payroll reporting.'},
    {'key': 'ca_c_940', 'num': 2, 'quarter': 'Q1', 'scope': 'Federal', 'short': '940 FUTA',
     'title': 'Annual Federal Unemployment Tax', 'due_type': 'fixed', 'due_month': 1, 'due_day': 31,
     'due_text': 'January 31', 'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/',
     'info': 'Federal unemployment tax.'},
    {'key': 'ca_c_1099', 'num': 3, 'quarter': 'Q1', 'scope': 'Federal', 'short': '1099-NEC',
     'title': 'Form 1099-NEC Filings', 'due_type': 'fixed', 'due_month': 1, 'due_day': 31, 'due_text': 'January 31',
     'portal_name': 'IRS FIRE', 'portal_url': 'https://fire.irs.gov/',
     'info': 'Required for unincorporated contractors.'},
    {'key': 'ca_c_w2', 'num': 4, 'quarter': 'Q1', 'scope': 'Federal', 'short': 'W-2 / W-3',
     'title': 'Wage and Tax Statements', 'due_type': 'fixed', 'due_month': 1, 'due_day': 31, 'due_text': 'January 31',
     'portal_name': 'SSA BSO', 'portal_url': 'https://www.ssa.gov/bso/',
     'info': 'Employer reporting of employee W-2 earnings.'},
    {'key': 'ca_c_de9_4', 'num': 5, 'quarter': 'Q1', 'scope': 'California', 'short': 'DE 9/9C Q4',
     'title': 'CA EDD Payroll Return - Q4', 'due_type': 'fixed', 'due_month': 1, 'due_day': 31,
     'due_text': 'January 31', 'portal_name': 'CA EDD', 'portal_url': 'https://edd.ca.gov/e-Services_for_Business.htm',
     'info': 'State payroll tax return.'},

    # March
    {'key': 'ca_c_osha', 'num': 6, 'quarter': 'Q1', 'scope': 'Federal', 'short': 'OSHA 300A',
     'title': 'Cal/OSHA Form 300A Summary', 'due_type': 'fixed', 'due_month': 3, 'due_day': 2, 'due_text': 'March 2',
     'portal_name': 'OSHA ITA', 'portal_url': 'https://www.osha.gov/injuryreporting/', 'info': 'Injury log summary.'},
    {'key': 'ca_c_aca', 'num': 7, 'quarter': 'Q1', 'scope': 'Federal', 'short': 'ACA Reporting',
     'title': '1094/1095-C Filing (If ALE)', 'due_type': 'fixed', 'due_month': 3, 'due_day': 31, 'due_text': 'March 31',
     'portal_name': 'IRS AIR', 'portal_url': 'https://www.irs.gov/e-file-providers/air',
     'info': 'Required if entity has 50+ FTEs.'},

    # April
    {'key': 'ca_c_prop', 'num': 8, 'quarter': 'Q2', 'scope': 'California', 'short': 'Form 571-L',
     'title': 'Business Property Statement', 'due_type': 'fixed', 'due_month': 4, 'due_day': 1, 'due_text': 'April 1',
     'portal_name': 'County Assessor', 'portal_url': 'https://www.calassessor.org/',
     'info': 'Unsecured property > $100k.'},
    {'key': 'ca_c_1120', 'num': 9, 'quarter': 'Q2', 'scope': 'Federal', 'short': 'Form 1120',
     'title': 'U.S. Corporation Income Tax Return', 'due_type': 'fixed', 'due_month': 4, 'due_day': 15,
     'due_text': 'April 15', 'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/',
     'info': 'Core federal income tax return.'},
    {'key': 'ca_c_1120w_1', 'num': 10, 'quarter': 'Q2', 'scope': 'Federal', 'short': '1120-W Q1',
     'title': 'Fed Est. Tax - Installment 1', 'due_type': 'fixed', 'due_month': 4, 'due_day': 15,
     'due_text': 'April 15', 'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/',
     'info': 'Estimated tax payment.'},
    {'key': 'ca_c_ftb100', 'num': 11, 'quarter': 'Q2', 'scope': 'California', 'short': 'FTB Form 100',
     'title': 'CA Corporate Franchise & Income Tax', 'due_type': 'fixed', 'due_month': 4, 'due_day': 15,
     'due_text': 'April 15', 'portal_name': 'FTB Web Pay', 'portal_url': 'https://www.ftb.ca.gov/pay/',
     'info': 'Standard CA C-Corp tax return.'},
    {'key': 'ca_c_100es_1', 'num': 12, 'quarter': 'Q2', 'scope': 'California', 'short': '100-ES Q1',
     'title': 'CA Est. Tax - Installment 1 (30%)', 'due_type': 'fixed', 'due_month': 4, 'due_day': 15,
     'due_text': 'April 15', 'portal_name': 'FTB Web Pay', 'portal_url': 'https://www.ftb.ca.gov/pay/',
     'info': 'First state estimated payment.'},
    {'key': 'ca_c_941_1', 'num': 13, 'quarter': 'Q2', 'scope': 'Federal', 'short': '941 Q1',
     'title': 'Federal Payroll Tax - Q1', 'due_type': 'fixed', 'due_month': 4, 'due_day': 30, 'due_text': 'April 30',
     'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/', 'info': 'Quarterly payroll reporting.'},
    {'key': 'ca_c_de9_1', 'num': 14, 'quarter': 'Q2', 'scope': 'California', 'short': 'DE 9/9C Q1',
     'title': 'CA EDD Payroll Return - Q1', 'due_type': 'fixed', 'due_month': 4, 'due_day': 30, 'due_text': 'April 30',
     'portal_name': 'CA EDD', 'portal_url': 'https://edd.ca.gov/e-Services_for_Business.htm',
     'info': 'State payroll tax return.'},

    # May
    {'key': 'ca_c_paydata', 'num': 15, 'quarter': 'Q2', 'scope': 'California', 'short': 'CA Pay Data',
     'title': 'CA Pay Data Report', 'due_type': 'fixed', 'due_month': 5, 'due_day': 13, 'due_text': 'May (2nd Wed)',
     'portal_name': 'CRD Portal', 'portal_url': 'https://calcivilrights.ca.gov/paydatareporting/',
     'info': 'Required for 100+ employees.'},

    # June
    {'key': 'ca_c_1120w_2', 'num': 16, 'quarter': 'Q2', 'scope': 'Federal', 'short': '1120-W Q2',
     'title': 'Fed Est. Tax - Installment 2', 'due_type': 'fixed', 'due_month': 6, 'due_day': 15, 'due_text': 'June 15',
     'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/', 'info': 'Estimated tax payment.'},
    {'key': 'ca_c_100es_2', 'num': 17, 'quarter': 'Q2', 'scope': 'California', 'short': '100-ES Q2',
     'title': 'CA Est. Tax - Installment 2 (40%)', 'due_type': 'fixed', 'due_month': 6, 'due_day': 15,
     'due_text': 'June 15', 'portal_name': 'FTB Web Pay', 'portal_url': 'https://www.ftb.ca.gov/pay/',
     'info': 'Second state estimated payment.'},

    # July
    {'key': 'ca_c_941_2', 'num': 18, 'quarter': 'Q3', 'scope': 'Federal', 'short': '941 Q2',
     'title': 'Federal Payroll Tax - Q2', 'due_type': 'fixed', 'due_month': 7, 'due_day': 31, 'due_text': 'July 31',
     'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/', 'info': 'Quarterly payroll reporting.'},
    {'key': 'ca_c_de9_2', 'num': 19, 'quarter': 'Q3', 'scope': 'California', 'short': 'DE 9/9C Q2',
     'title': 'CA EDD Payroll Return - Q2', 'due_type': 'fixed', 'due_month': 7, 'due_day': 31, 'due_text': 'July 31',
     'portal_name': 'CA EDD', 'portal_url': 'https://edd.ca.gov/e-Services_for_Business.htm',
     'info': 'State payroll tax return.'},
    {'key': 'ca_c_5500', 'num': 20, 'quarter': 'Q3', 'scope': 'Federal', 'short': 'Form 5500',
     'title': 'Employee Benefit Plan Report', 'due_type': 'fixed', 'due_month': 7, 'due_day': 31, 'due_text': 'July 31',
     'portal_name': 'EFAST2', 'portal_url': 'https://www.efast.dol.gov/', 'info': 'For 401k/health plans.'},

    # September
    {'key': 'ca_c_1120w_3', 'num': 21, 'quarter': 'Q3', 'scope': 'Federal', 'short': '1120-W Q3',
     'title': 'Fed Est. Tax - Installment 3', 'due_type': 'fixed', 'due_month': 9, 'due_day': 15,
     'due_text': 'September 15', 'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/',
     'info': 'Estimated tax payment.'},
    {'key': 'ca_c_100es_3', 'num': 22, 'quarter': 'Q3', 'scope': 'California', 'short': '100-ES Q3',
     'title': 'CA Est. Tax - Installment 3 (0%)', 'due_type': 'fixed', 'due_month': 9, 'due_day': 15,
     'due_text': 'September 15', 'portal_name': 'FTB Web Pay', 'portal_url': 'https://www.ftb.ca.gov/pay/',
     'info': 'Third state estimated payment (0%).'},

    # October
    {'key': 'ca_c_941_3', 'num': 23, 'quarter': 'Q4', 'scope': 'Federal', 'short': '941 Q3',
     'title': 'Federal Payroll Tax - Q3', 'due_type': 'fixed', 'due_month': 10, 'due_day': 31, 'due_text': 'October 31',
     'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/', 'info': 'Quarterly payroll reporting.'},
    {'key': 'ca_c_de9_3', 'num': 24, 'quarter': 'Q4', 'scope': 'California', 'short': 'DE 9/9C Q3',
     'title': 'CA EDD Payroll Return - Q3', 'due_type': 'fixed', 'due_month': 10, 'due_day': 31,
     'due_text': 'October 31', 'portal_name': 'CA EDD', 'portal_url': 'https://edd.ca.gov/e-Services_for_Business.htm',
     'info': 'State payroll tax return.'},

    # November
    {'key': 'ca_c_esch', 'num': 25, 'quarter': 'Q4', 'scope': 'California', 'short': 'CA Escheatment',
     'title': 'CA Unclaimed Property Holder Report', 'due_type': 'fixed', 'due_month': 11, 'due_day': 1,
     'due_text': 'November 1', 'portal_name': 'State Controller', 'portal_url': 'https://www.sco.ca.gov/upd_rptg.html',
     'info': 'Report of unclaimed checks/assets.'},

    # December
    {'key': 'ca_c_1120w_4', 'num': 26, 'quarter': 'Q4', 'scope': 'Federal', 'short': '1120-W Q4',
     'title': 'Fed Est. Tax - Installment 4', 'due_type': 'fixed', 'due_month': 12, 'due_day': 15,
     'due_text': 'December 15', 'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/',
     'info': 'Estimated tax payment.'},
    {'key': 'ca_c_100es_4', 'num': 27, 'quarter': 'Q4', 'scope': 'California', 'short': '100-ES Q4',
     'title': 'CA Est. Tax - Installment 4 (30%)', 'due_type': 'fixed', 'due_month': 12, 'due_day': 15,
     'due_text': 'December 15', 'portal_name': 'FTB Web Pay', 'portal_url': 'https://www.ftb.ca.gov/pay/',
     'info': 'Final state estimated payment.'},

    # Rolling / Anniversary Deadlines
    {'key': 'ca_c_boi', 'num': 28, 'quarter': 'ROLL', 'scope': 'Federal', 'short': 'FinCEN BOI',
     'title': 'Beneficial Ownership Information', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
     'due_text': 'Exempt for U.S.-domestic entities (as of 2025)', 'portal_name': 'FinCEN E-Filing',
     'portal_url': 'https://boiefiling.fincen.gov/',
     'info': "Exempt for U.S.-formed entities under FinCEN's March 2025 interim final rule — only foreign companies registered to do business in the U.S. must still file. Monitor FinCEN.gov for changes."},
    {'key': 'ca_c_newhire', 'num': 29, 'quarter': 'ROLL', 'scope': 'California', 'short': 'DE 34',
     'title': 'CA EDD Report of New Hire', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
     'due_text': 'Within 20 days of hire', 'portal_name': 'CA EDD',
     'portal_url': 'https://edd.ca.gov/e-Services_for_Business.htm', 'info': 'Mandatory onboarding reporting.'},
    {'key': 'ca_c_ic', 'num': 30, 'quarter': 'ROLL', 'scope': 'California', 'short': 'DE 542',
     'title': 'CA EDD Independent Contractor Report', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
     'due_text': 'Within 20 days of $600 payment', 'portal_name': 'CA EDD',
     'portal_url': 'https://edd.ca.gov/e-Services_for_Business.htm', 'info': 'Mandatory 1099 reporting.'},
    {'key': 'ca_c_si200', 'num': 31, 'quarter': 'ROLL', 'scope': 'California', 'short': 'Form SI-200',
     'title': 'Statement of Information (Domestic)', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
     'due_text': 'Annually', 'portal_name': 'bizfile Online', 'portal_url': 'https://bizfileonline.sos.ca.gov/',
     'info': 'File in the anniversary month of incorporation.'},
    {'key': 'ca_c_local', 'num': 32, 'quarter': 'ROLL', 'scope': 'Local', 'short': 'Biz License',
     'title': 'Local Business License', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
     'due_text': 'Annually', 'portal_name': 'City Portal', 'portal_url': 'https://www.walnut-creek.org/',
     'info': 'Local operational tax.'},
    {'key': 'ca_c_agent', 'num': 33, 'quarter': 'ROLL', 'scope': 'California', 'short': 'Reg. Agent',
     'title': 'Registered Agent Annual Renewal', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
     'due_text': 'Annually', 'portal_name': 'Agent Portal', 'portal_url': 'https://www.vcorpservices.com/',
     'info': 'Maintains legal good standing in the state of incorporation.'},
    {'key': 'ca_c_minutes', 'num': 34, 'quarter': 'ROLL', 'scope': 'Internal', 'short': 'Corp Minutes',
     'title': 'Annual Board/Shareholder Minutes', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
     'due_text': 'Annually', 'portal_name': 'Internal', 'portal_url': '#', 'info': 'Corporate formalities.'},
    {'key': 'ca_c_ins', 'num': 35, 'quarter': 'ROLL', 'scope': 'Insurance', 'short': 'Corp Insurances',
     'title': 'General/D&O/WC Insurance Renewals', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
     'due_text': 'Annually', 'portal_name': 'Broker', 'portal_url': '#', 'info': 'Liability matrix.'}
]

DELAWARE_CCORP_TASKS = [
    # January
    {'key': 'de_c_941_4', 'num': 1, 'quarter': 'Q1', 'scope': 'Federal', 'short': '941 Q4',
     'title': 'Federal Payroll Tax - Q4', 'due_type': 'fixed', 'due_month': 1, 'due_day': 31, 'due_text': 'January 31',
     'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/', 'info': 'Payroll reporting.'},
    {'key': 'de_c_940', 'num': 2, 'quarter': 'Q1', 'scope': 'Federal', 'short': '940 FUTA',
     'title': 'Annual Federal Unemployment Tax', 'due_type': 'fixed', 'due_month': 1, 'due_day': 31,
     'due_text': 'January 31', 'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/',
     'info': 'Federal unemployment tax.'},
    {'key': 'de_c_1099', 'num': 3, 'quarter': 'Q1', 'scope': 'Federal', 'short': '1099-NEC',
     'title': 'Form 1099-NEC Filings', 'due_type': 'fixed', 'due_month': 1, 'due_day': 31, 'due_text': 'January 31',
     'portal_name': 'IRS FIRE', 'portal_url': 'https://fire.irs.gov/', 'info': 'Contractor reporting.'},
    {'key': 'de_c_w2', 'num': 4, 'quarter': 'Q1', 'scope': 'Federal', 'short': 'W-2 / W-3',
     'title': 'Wage and Tax Statements', 'due_type': 'fixed', 'due_month': 1, 'due_day': 31, 'due_text': 'January 31',
     'portal_name': 'SSA BSO', 'portal_url': 'https://www.ssa.gov/bso/', 'info': 'Employee earnings reporting.'},

    # March
    {'key': 'de_c_ar', 'num': 5, 'quarter': 'Q1', 'scope': 'Delaware', 'short': 'DE Annual Report',
     'title': 'Delaware Annual Report & Franchise Tax', 'due_type': 'fixed', 'due_month': 3, 'due_day': 1,
     'due_text': 'March 1', 'portal_name': 'DE Division of Corps',
     'portal_url': 'https://icis.corp.delaware.gov/ecorp/',
     'info': 'Required annually. Minimum franchise tax is $175 plus a $50 filing fee.'},
    {'key': 'de_c_esch', 'num': 6, 'quarter': 'Q1', 'scope': 'Delaware', 'short': 'DE Escheatment',
     'title': 'DE Unclaimed Property Report', 'due_type': 'fixed', 'due_month': 3, 'due_day': 1, 'due_text': 'March 1',
     'portal_name': 'DE Dept of Finance', 'portal_url': 'https://unclaimedproperty.delaware.gov/',
     'info': 'Filing required even if there is no unclaimed property (Negative Report).'},
    {'key': 'de_c_osha', 'num': 7, 'quarter': 'Q1', 'scope': 'Federal', 'short': 'OSHA 300A',
     'title': 'OSHA Form 300A Summary Submission', 'due_type': 'fixed', 'due_month': 3, 'due_day': 2,
     'due_text': 'March 2', 'portal_name': 'OSHA ITA', 'portal_url': 'https://www.osha.gov/injuryreporting/',
     'info': 'Electronic submission of work-related injuries/illnesses summary.'},
    {'key': 'de_c_aca', 'num': 8, 'quarter': 'Q1', 'scope': 'Federal', 'short': 'ACA 1094/1095-C',
     'title': 'Affordable Care Act Employer Reporting', 'due_type': 'fixed', 'due_month': 3, 'due_day': 31,
     'due_text': 'March 31', 'portal_name': 'IRS AIR', 'portal_url': 'https://www.irs.gov/e-file-providers/air',
     'info': 'Electronic filing deadline. Required for Applicable Large Employers (50+ FTEs).'},

    # April
    {'key': 'de_c_1120', 'num': 9, 'quarter': 'Q2', 'scope': 'Federal', 'short': 'Form 1120',
     'title': 'U.S. Corporation Income Tax Return', 'due_type': 'fixed', 'due_month': 4, 'due_day': 15,
     'due_text': 'April 15', 'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/',
     'info': 'Federal C-Corporation tax return.'},
    {'key': 'de_c_1120w_1', 'num': 10, 'quarter': 'Q2', 'scope': 'Federal', 'short': '1120-W Q1',
     'title': 'Fed Est. Tax - Installment 1', 'due_type': 'fixed', 'due_month': 4, 'due_day': 15,
     'due_text': 'April 15', 'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/',
     'info': 'Estimated tax.'},
    {'key': 'de_c_1100', 'num': 11, 'quarter': 'Q2', 'scope': 'Delaware', 'short': 'Form 1100',
     'title': 'Delaware Corporate Income Tax Return', 'due_type': 'fixed', 'due_month': 4, 'due_day': 15,
     'due_text': 'April 15', 'portal_name': 'DE Taxpayer Portal', 'portal_url': 'https://tax.delaware.gov/',
     'info': '8.7% flat tax applied to corporate net income apportioned to Delaware.'},
    {'key': 'de_c_est_1', 'num': 12, 'quarter': 'Q2', 'scope': 'Delaware', 'short': 'DE Est. Tax Q1',
     'title': 'DE Est. Corporate Income Tax - Q1', 'due_type': 'fixed', 'due_month': 4, 'due_day': 15,
     'due_text': 'April 15', 'portal_name': 'DE Taxpayer Portal', 'portal_url': 'https://tax.delaware.gov/',
     'info': 'State estimated tax.'},
    {'key': 'de_c_941_1', 'num': 13, 'quarter': 'Q2', 'scope': 'Federal', 'short': '941 Q1',
     'title': 'Federal Payroll Tax - Q1', 'due_type': 'fixed', 'due_month': 4, 'due_day': 30, 'due_text': 'April 30',
     'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/', 'info': 'Payroll reporting.'},

    # June
    {'key': 'de_c_1120w_2', 'num': 14, 'quarter': 'Q2', 'scope': 'Federal', 'short': '1120-W Q2',
     'title': 'Fed Est. Tax - Installment 2', 'due_type': 'fixed', 'due_month': 6, 'due_day': 15, 'due_text': 'June 15',
     'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/', 'info': 'Estimated tax.'},
    {'key': 'de_c_est_2', 'num': 15, 'quarter': 'Q2', 'scope': 'Delaware', 'short': 'DE Est. Tax Q2',
     'title': 'DE Est. Corporate Income Tax - Q2', 'due_type': 'fixed', 'due_month': 6, 'due_day': 15,
     'due_text': 'June 15', 'portal_name': 'DE Taxpayer Portal', 'portal_url': 'https://tax.delaware.gov/',
     'info': 'State estimated tax.'},

    # July
    {'key': 'de_c_941_2', 'num': 16, 'quarter': 'Q3', 'scope': 'Federal', 'short': '941 Q2',
     'title': 'Federal Payroll Tax - Q2', 'due_type': 'fixed', 'due_month': 7, 'due_day': 31, 'due_text': 'July 31',
     'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/', 'info': 'Payroll reporting.'},
    {'key': 'de_c_5500', 'num': 17, 'quarter': 'Q3', 'scope': 'Federal', 'short': 'Form 5500',
     'title': 'Annual Return/Report of Employee Benefit Plan', 'due_type': 'fixed', 'due_month': 7, 'due_day': 31,
     'due_text': 'July 31', 'portal_name': 'EFAST2', 'portal_url': 'https://www.efast.dol.gov/',
     'info': 'Required for 401(k) plans and health/welfare plans with 100+ participants.'},

    # September
    {'key': 'de_c_1120w_3', 'num': 18, 'quarter': 'Q3', 'scope': 'Federal', 'short': '1120-W Q3',
     'title': 'Fed Est. Tax - Installment 3', 'due_type': 'fixed', 'due_month': 9, 'due_day': 15,
     'due_text': 'September 15', 'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/',
     'info': 'Estimated tax.'},
    {'key': 'de_c_est_3', 'num': 19, 'quarter': 'Q3', 'scope': 'Delaware', 'short': 'DE Est. Tax Q3',
     'title': 'DE Est. Corporate Income Tax - Q3', 'due_type': 'fixed', 'due_month': 9, 'due_day': 15,
     'due_text': 'September 15', 'portal_name': 'DE Taxpayer Portal', 'portal_url': 'https://tax.delaware.gov/',
     'info': 'State estimated tax.'},

    # October
    {'key': 'de_c_941_3', 'num': 20, 'quarter': 'Q4', 'scope': 'Federal', 'short': '941 Q3',
     'title': 'Federal Payroll Tax - Q3', 'due_type': 'fixed', 'due_month': 10, 'due_day': 31, 'due_text': 'October 31',
     'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/', 'info': 'Payroll reporting.'},

    # December
    {'key': 'de_c_1120w_4', 'num': 21, 'quarter': 'Q4', 'scope': 'Federal', 'short': '1120-W Q4',
     'title': 'Fed Est. Tax - Installment 4', 'due_type': 'fixed', 'due_month': 12, 'due_day': 15,
     'due_text': 'December 15', 'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/',
     'info': 'Estimated tax.'},
    {'key': 'de_c_est_4', 'num': 22, 'quarter': 'Q4', 'scope': 'Delaware', 'short': 'DE Est. Tax Q4',
     'title': 'DE Est. Corporate Income Tax - Q4', 'due_type': 'fixed', 'due_month': 12, 'due_day': 15,
     'due_text': 'December 15', 'portal_name': 'DE Taxpayer Portal', 'portal_url': 'https://tax.delaware.gov/',
     'info': 'State estimated tax.'},

    # Rolling / Anniversary Deadlines
    {'key': 'de_c_boi', 'num': 23, 'quarter': 'ROLL', 'scope': 'Federal', 'short': 'FinCEN BOI',
     'title': 'Beneficial Ownership Information', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
     'due_text': 'Exempt for U.S.-domestic entities (as of 2025)', 'portal_name': 'FinCEN E-Filing',
     'portal_url': 'https://boiefiling.fincen.gov/',
     'info': "Exempt for U.S.-formed entities under FinCEN's March 2025 interim final rule — only foreign companies registered to do business in the U.S. must still file. Monitor FinCEN.gov for changes."},
    {'key': 'de_c_grt', 'num': 24, 'quarter': 'ROLL', 'scope': 'Delaware', 'short': 'DE Gross Receipts',
     'title': 'Delaware Gross Receipts Tax', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
     'due_text': 'Monthly/Quarterly based on volume', 'portal_name': 'DE Taxpayer Portal',
     'portal_url': 'https://tax.delaware.gov/',
     'info': 'Required if operating physically in DE.'},
    {'key': 'de_c_agent', 'num': 25, 'quarter': 'ROLL', 'scope': 'Delaware', 'short': 'Registered Agent',
     'title': 'DE Registered Agent Renewal', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
     'due_text': 'Annually', 'portal_name': 'Agent Portal', 'portal_url': 'https://www.vcorpservices.com/',
     'info': 'Failure to pay results in resignation and loss of corporate good standing.'},
    {'key': 'de_c_minutes', 'num': 26, 'quarter': 'ROLL', 'scope': 'Internal', 'short': 'Board Minutes',
     'title': 'Annual Board of Directors Meetings & Minutes', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
     'due_text': 'Annually', 'portal_name': 'Internal', 'portal_url': '#',
     'info': 'Execute Unanimous Written Consents.'},
    {'key': 'de_c_foreign', 'num': 27, 'quarter': 'ROLL', 'scope': 'State', 'short': 'Foreign Qual.',
     'title': 'Foreign Qualification Annual Reports', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
     'due_text': 'Varies by operating state', 'portal_name': 'Foreign SOS',
     'portal_url': 'https://www.usa.gov/state-government',
     'info': 'Maintain good standing in states where the C-Corp has operations.'},
    {'key': 'de_c_gl', 'num': 28, 'quarter': 'ROLL', 'scope': 'Insurance', 'short': 'Gen. Liab.',
     'title': 'General Liability Insurance Renewal', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
     'due_text': 'Annually', 'portal_name': 'Broker', 'portal_url': '#',
     'info': 'Covers physical premise injuries and property damage.'},
    {'key': 'de_c_do', 'num': 29, 'quarter': 'ROLL', 'scope': 'Insurance', 'short': 'D&O Insurance',
     'title': 'Directors & Officers Liability Insurance', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
     'due_text': 'Annually', 'portal_name': 'Broker', 'portal_url': '#',
     'info': 'Protects board members from personal liability.'},
    {'key': 'de_c_wc', 'num': 30, 'quarter': 'ROLL', 'scope': 'Insurance', 'short': 'Workers Comp',
     'title': 'Workers Compensation Insurance Renewal', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
     'due_text': 'Annually', 'portal_name': 'Broker', 'portal_url': '#',
     'info': 'Statutory requirement in most states for any W-2 employees.'}
]

PEBBLE_TASKS = [
    # January
    {'key': 'peb_592', 'num': 1, 'quarter': 'Q1', 'scope': 'California', 'short': 'Form 592',
     'title': 'CA Resident/Nonresident Withholding', 'due_type': 'fixed', 'due_month': 1, 'due_day': 31,
     'due_text': 'January 31', 'portal_name': 'FTB Web Pay', 'portal_url': 'https://www.ftb.ca.gov/pay/',
     'info': 'Withholding on CA source income distributed to members.'},
    {'key': 'peb_941q4', 'num': 2, 'quarter': 'Q1', 'scope': 'Federal', 'short': '941 Q4',
     'title': 'Federal Payroll Tax Return - Q4', 'due_type': 'fixed', 'due_month': 1, 'due_day': 31,
     'due_text': 'January 31', 'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/',
     'info': 'Quarterly payroll reporting.'},
    {'key': 'peb_940', 'num': 3, 'quarter': 'Q1', 'scope': 'Federal', 'short': '940 FUTA',
     'title': 'Federal Unemployment Tax Return', 'due_type': 'fixed', 'due_month': 1, 'due_day': 31,
     'due_text': 'January 31', 'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/',
     'info': 'Annual FUTA reconciliation.'},
    {'key': 'peb_w2', 'num': 4, 'quarter': 'Q1', 'scope': 'Federal', 'short': 'W-2 / W-3',
     'title': 'Wage and Tax Statements', 'due_type': 'fixed', 'due_month': 1, 'due_day': 31, 'due_text': 'January 31',
     'portal_name': 'SSA BSO', 'portal_url': 'https://www.ssa.gov/bso/', 'info': 'Transmittal of employee earnings.'},
    {'key': 'peb_1099', 'num': 5, 'quarter': 'Q1', 'scope': 'Federal', 'short': '1099-NEC',
     'title': 'Form 1099-NEC Filing', 'due_type': 'fixed', 'due_month': 1, 'due_day': 31, 'due_text': 'January 31',
     'portal_name': 'IRS FIRE', 'portal_url': 'https://fire.irs.gov/',
     'info': 'Required for unincorporated contractors paid $600+.'},
    {'key': 'peb_de9q4', 'num': 6, 'quarter': 'Q1', 'scope': 'California', 'short': 'CA DE 9/9C Q4',
     'title': 'CA EDD Quarterly Payroll Return - Q4', 'due_type': 'fixed', 'due_month': 1, 'due_day': 31,
     'due_text': 'January 31', 'portal_name': 'EDD e-Services',
     'portal_url': 'https://edd.ca.gov/e-Services_for_Business.htm', 'info': 'California state payroll.'},

    # March
    {'key': 'peb_fed1065', 'num': 7, 'quarter': 'Q1', 'scope': 'Federal', 'short': 'Form 1065',
     'title': 'US Return of Partnership Income', 'due_type': 'fixed', 'due_month': 3, 'due_day': 15,
     'due_text': 'March 15', 'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/',
     'info': 'Federal tax return for multi-member LLCs. Generates Schedule K-1s.'},
    {'key': 'peb_ftb568', 'num': 8, 'quarter': 'Q1', 'scope': 'California', 'short': 'FTB 568',
     'title': 'CA LLC Return of Income', 'due_type': 'fixed', 'due_month': 3, 'due_day': 15, 'due_text': 'March 15',
     'portal_name': 'FTB Web Pay', 'portal_url': 'https://www.ftb.ca.gov/pay/',
     'info': 'Annual income return for multi-member CA LLCs taxed as partnerships.'},

    # April
    {'key': 'peb_571l', 'num': 9, 'quarter': 'Q2', 'scope': 'California', 'short': 'Form 571-L',
     'title': 'Business Property Statement', 'due_type': 'fixed', 'due_month': 4, 'due_day': 1, 'due_text': 'April 1',
     'portal_name': 'County Assessor', 'portal_url': 'https://www.calassessor.org/',
     'info': 'Required if CA unsecured business property exceeds $100k.'},
    {'key': 'peb_ftb3522', 'num': 10, 'quarter': 'Q2', 'scope': 'California', 'short': 'FTB 3522',
     'title': 'CA LLC Annual Tax Voucher ($800 Minimum)', 'due_type': 'fixed', 'due_month': 4, 'due_day': 15,
     'due_text': 'April 15', 'portal_name': 'FTB Web Pay', 'portal_url': 'https://www.ftb.ca.gov/pay/',
     'info': 'Statutory minimum California franchise tax required for all LLCs doing business in the state.'},
    {'key': 'peb_941q1', 'num': 11, 'quarter': 'Q2', 'scope': 'Federal', 'short': '941 Q1',
     'title': 'Federal Payroll Tax Return - Q1', 'due_type': 'fixed', 'due_month': 4, 'due_day': 30,
     'due_text': 'April 30', 'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/',
     'info': 'Quarterly reporting of employee payroll withholdings.'},
    {'key': 'peb_de9q1', 'num': 12, 'quarter': 'Q2', 'scope': 'California', 'short': 'CA DE 9/9C Q1',
     'title': 'CA EDD Quarterly Payroll Return - Q1', 'due_type': 'fixed', 'due_month': 4, 'due_day': 30,
     'due_text': 'April 30', 'portal_name': 'EDD e-Services',
     'portal_url': 'https://edd.ca.gov/e-Services_for_Business.htm',
     'info': 'California state payroll and unemployment reporting.'},

    # June
    {'key': 'peb_ftb3536', 'num': 13, 'quarter': 'Q2', 'scope': 'California', 'short': 'FTB 3536',
     'title': 'CA LLC Estimated Fee', 'due_type': 'fixed', 'due_month': 6, 'due_day': 15, 'due_text': 'June 15',
     'portal_name': 'FTB Web Pay', 'portal_url': 'https://www.ftb.ca.gov/pay/',
     'info': 'Only applies if gross CA receipts exceed $250,000.'},

    # July
    {'key': 'peb_941q2', 'num': 14, 'quarter': 'Q3', 'scope': 'Federal', 'short': '941 Q2',
     'title': 'Federal Payroll Tax Return - Q2', 'due_type': 'fixed', 'due_month': 7, 'due_day': 31,
     'due_text': 'July 31', 'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/',
     'info': 'Quarterly payroll reporting.'},
    {'key': 'peb_de9q2', 'num': 15, 'quarter': 'Q3', 'scope': 'California', 'short': 'CA DE 9/9C Q2',
     'title': 'CA EDD Quarterly Payroll Return - Q2', 'due_type': 'fixed', 'due_month': 7, 'due_day': 31,
     'due_text': 'July 31', 'portal_name': 'EDD e-Services',
     'portal_url': 'https://edd.ca.gov/e-Services_for_Business.htm', 'info': 'California state payroll.'},

    # October
    {'key': 'peb_941q3', 'num': 16, 'quarter': 'Q4', 'scope': 'Federal', 'short': '941 Q3',
     'title': 'Federal Payroll Tax Return - Q3', 'due_type': 'fixed', 'due_month': 10, 'due_day': 31,
     'due_text': 'October 31', 'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/',
     'info': 'Quarterly payroll reporting.'},
    {'key': 'peb_de9q3', 'num': 17, 'quarter': 'Q4', 'scope': 'California', 'short': 'CA DE 9/9C Q3',
     'title': 'CA EDD Quarterly Payroll Return - Q3', 'due_type': 'fixed', 'due_month': 10, 'due_day': 31,
     'due_text': 'October 31', 'portal_name': 'EDD e-Services',
     'portal_url': 'https://edd.ca.gov/e-Services_for_Business.htm', 'info': 'California state payroll.'},

    # Rolling / Anniversary Deadlines
    {'key': 'peb_boi', 'num': 18, 'quarter': 'ROLL', 'scope': 'Federal', 'short': 'FinCEN BOI',
     'title': 'Beneficial Ownership Information Report', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
     'due_text': 'Exempt for U.S.-domestic entities (as of 2025)', 'portal_name': 'FinCEN E-Filing',
     'portal_url': 'https://boiefiling.fincen.gov/',
     'info': "Exempt under FinCEN's March 2025 interim final rule, which excuses all U.S.-formed entities (including Pebble Impact LLC) from BOI reporting — only foreign companies registered to do business in the U.S. must still file. Monitor FinCEN.gov for changes."},
    {'key': 'peb_soi', 'num': 19, 'quarter': 'ROLL', 'scope': 'California', 'short': 'CA LLC-20',
     'title': 'Statement of Information (Form LLC-20)', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
     'due_text': 'Biennially', 'portal_name': 'bizfile Online', 'portal_url': 'https://bizfileonline.sos.ca.gov/',
     'info': 'Required for CA LLCs to maintain good standing. Filed every two years.'},
    {'key': 'peb_newhire', 'num': 20, 'quarter': 'ROLL', 'scope': 'California', 'short': 'DE 34',
     'title': 'CA EDD Report of New Hire', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
     'due_text': 'Within 20 days of hire', 'portal_name': 'CA EDD',
     'portal_url': 'https://edd.ca.gov/e-Services_for_Business.htm', 'info': 'Mandatory onboarding reporting.'},
    {'key': 'peb_ic', 'num': 21, 'quarter': 'ROLL', 'scope': 'California', 'short': 'DE 542',
     'title': 'CA EDD Independent Contractor Report', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
     'due_text': 'Within 20 days of $600 payment', 'portal_name': 'CA EDD',
     'portal_url': 'https://edd.ca.gov/e-Services_for_Business.htm', 'info': 'Mandatory 1099 reporting.'},
    {'key': 'peb_localbiz', 'num': 22, 'quarter': 'ROLL', 'scope': 'Local', 'short': 'Local Biz License',
     'title': 'Local Municipal Business License Renewal', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
     'due_text': 'Annually before expiration', 'portal_name': 'City Business Portal',
     'portal_url': 'https://www.walnut-creek.org/',
     'info': 'Required by the local California city/county to legally operate.'},
    {'key': 'peb_minutes', 'num': 23, 'quarter': 'ROLL', 'scope': 'Internal', 'short': 'Operating Agreement',
     'title': 'Annual Review of LLC Operating Agreement', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
     'due_text': 'Annually', 'portal_name': 'Internal Records', 'portal_url': '#',
     'info': 'Annual member meetings and documented resolutions ensure liability protection.'}
]

NON_PROFIT_TASKS = [
    # January
    {'key': 'np_941q4', 'num': 1, 'quarter': 'Q1', 'scope': 'Federal', 'short': 'Form 941 Q4',
     'title': 'Employer’s Quarterly Federal Tax Return - Q4', 'due_type': 'fixed', 'due_month': 1, 'due_day': 31,
     'due_text': 'January 31', 'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/',
     'info': 'Payroll reporting.'},
    {'key': 'np_w2', 'num': 2, 'quarter': 'Q1', 'scope': 'Federal', 'short': 'W-2 / W-3',
     'title': 'Wage and Tax Statements', 'due_type': 'fixed', 'due_month': 1, 'due_day': 31, 'due_text': 'January 31',
     'portal_name': 'SSA BSO', 'portal_url': 'https://www.ssa.gov/bso/', 'info': 'Required for employees.'},
    {'key': 'np_1099', 'num': 3, 'quarter': 'Q1', 'scope': 'Federal', 'short': '1099-NEC',
     'title': 'Form 1099-NEC Filings', 'due_type': 'fixed', 'due_month': 1, 'due_day': 31, 'due_text': 'January 31',
     'portal_name': 'IRS FIRE', 'portal_url': 'https://fire.irs.gov/',
     'info': 'Required for unincorporated contractors.'},

    # April
    {'key': 'np_941q1', 'num': 4, 'quarter': 'Q2', 'scope': 'Federal', 'short': 'Form 941 Q1',
     'title': 'Employer’s Quarterly Federal Tax Return - Q1', 'due_type': 'fixed', 'due_month': 4, 'due_day': 30,
     'due_text': 'April 30', 'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/',
     'info': 'Reports federal income tax withholding. Required even if tax-exempt.'},

    # May
    {'key': 'np_990', 'num': 5, 'quarter': 'Q2', 'scope': 'Federal', 'short': 'Form 990',
     'title': 'Return of Organization Exempt From Income Tax', 'due_type': 'fixed', 'due_month': 5, 'due_day': 15,
     'due_text': 'May 15', 'portal_name': 'IRS e-file',
     'portal_url': 'https://www.irs.gov/e-file-providers/e-file-for-charities-and-non-profits',
     'info': 'Annual informational return (990, 990-EZ, or 990-N). Failure to file for 3 consecutive years revokes exempt status.'},
    {'key': 'np_990t', 'num': 6, 'quarter': 'Q2', 'scope': 'Federal', 'short': 'Form 990-T',
     'title': 'Exempt Organization Business Income Tax Return', 'due_type': 'fixed', 'due_month': 5, 'due_day': 15,
     'due_text': 'May 15', 'portal_name': 'IRS e-file',
     'portal_url': 'https://www.irs.gov/e-file-providers/e-file-for-charities-and-non-profits',
     'info': 'Only required if the organization has $1,000+ of gross unrelated business taxable income.'},

    # July
    {'key': 'np_941q2', 'num': 7, 'quarter': 'Q3', 'scope': 'Federal', 'short': 'Form 941 Q2',
     'title': 'Employer’s Quarterly Federal Tax Return - Q2', 'due_type': 'fixed', 'due_month': 7, 'due_day': 31,
     'due_text': 'July 31', 'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/',
     'info': 'Payroll reporting.'},

    # October
    {'key': 'np_941q3', 'num': 8, 'quarter': 'Q4', 'scope': 'Federal', 'short': 'Form 941 Q3',
     'title': 'Employer’s Quarterly Federal Tax Return - Q3', 'due_type': 'fixed', 'due_month': 10, 'due_day': 31,
     'due_text': 'October 31', 'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/',
     'info': 'Payroll reporting.'},

    # Rolling / Anniversary Deadlines
    {'key': 'np_charity_reg', 'num': 9, 'quarter': 'ROLL', 'scope': 'State', 'short': 'Charitable Reg.',
     'title': 'State Charitable Solicitation Registration', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
     'due_text': 'Annually', 'portal_name': 'State AG Portal', 'portal_url': 'https://oag.ca.gov/charities',
     'info': 'Registration with the Attorney General before soliciting donations.'},
    {'key': 'np_ag_report', 'num': 10, 'quarter': 'ROLL', 'scope': 'State', 'short': 'AG Financials',
     'title': 'Attorney General Annual Charity Financial Report', 'due_type': 'rolling', 'due_month': None,
     'due_day': None, 'due_text': 'Annually', 'portal_name': 'State Charities Bureau',
     'portal_url': 'https://oag.ca.gov/charities',
     'info': 'Separate from Form 990. State-specific annual financial disclosure.'},
    {'key': 'np_soi', 'num': 11, 'quarter': 'ROLL', 'scope': 'State', 'short': 'Corp Report',
     'title': 'Secretary of State Annual/Biennial Report', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
     'due_text': 'Annually/Biennially', 'portal_name': 'Secretary of State Portal',
     'portal_url': 'https://bizfileonline.sos.ca.gov/',
     'info': 'Keeps the nonprofit corporate entity in good standing.'},
    {'key': 'np_property', 'num': 12, 'quarter': 'ROLL', 'scope': 'State', 'short': 'Property Exemption',
     'title': 'Welfare / Property Tax Exemption Claim', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
     'due_text': 'Varies locally', 'portal_name': 'County Assessor', 'portal_url': 'https://www.calassessor.org/',
     'info': 'Claim a charitable exemption if property is owned.'},
    {'key': 'np_sales_ex', 'num': 13, 'quarter': 'ROLL', 'scope': 'State', 'short': 'Sales Tax Exemp',
     'title': 'Sales Tax Exemption Certificate Renewal', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
     'due_text': 'Varies by State', 'portal_name': 'State Dept of Rev',
     'portal_url': 'https://www.usa.gov/state-government',
     'info': 'Renews the organization\'s ability to purchase goods tax-free.'},
    {'key': 'np_donors', 'num': 14, 'quarter': 'ROLL', 'scope': 'Internal', 'short': 'Donor Letters',
     'title': 'Contemporaneous Written Acknowledgment for Donors', 'due_type': 'rolling', 'due_month': None,
     'due_day': None, 'due_text': 'Continuous', 'portal_name': 'Internal CRM', 'portal_url': '#',
     'info': 'IRS requires written acknowledgments for any single contribution of $250+.'},
    {'key': 'np_coi', 'num': 15, 'quarter': 'ROLL', 'scope': 'Internal', 'short': 'COI Policy',
     'title': 'Annual Conflict of Interest Policy Disclosures', 'due_type': 'rolling', 'due_month': None,
     'due_day': None, 'due_text': 'Annually', 'portal_name': 'Internal Records', 'portal_url': '#',
     'info': 'Annual signed disclosures document compliance for the Form 990.'},
    {'key': 'np_do_ins', 'num': 16, 'quarter': 'ROLL', 'scope': 'Insurance', 'short': 'D&O Insurance',
     'title': 'Directors & Officers Liability Insurance', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
     'due_text': 'Annually', 'portal_name': 'Broker', 'portal_url': '#',
     'info': 'Protects board members from personal liability.'}
]

GENERAL_LLC_TASKS = [
    # January
    {'key': 'gen_1099', 'num': 1, 'quarter': 'Q1', 'scope': 'Federal', 'short': '1099-NEC',
     'title': 'Form 1099-NEC Filings', 'due_type': 'fixed', 'due_month': 1, 'due_day': 31, 'due_text': 'January 31',
     'portal_name': 'IRS FIRE', 'portal_url': 'https://fire.irs.gov/',
     'info': 'Distribute to independent contractors paid $600+.'},
    {'key': 'gen_w2', 'num': 2, 'quarter': 'Q1', 'scope': 'Federal', 'short': 'W-2 / W-3',
     'title': 'Wage and Tax Statements', 'due_type': 'fixed', 'due_month': 1, 'due_day': 31, 'due_text': 'January 31',
     'portal_name': 'SSA BSO', 'portal_url': 'https://www.ssa.gov/bso/', 'info': 'Employee earnings reporting.'},
    {'key': 'gen_941_4', 'num': 3, 'quarter': 'Q1', 'scope': 'Federal', 'short': '941 Q4',
     'title': 'Federal Payroll Tax - Q4', 'due_type': 'fixed', 'due_month': 1, 'due_day': 31, 'due_text': 'January 31',
     'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/', 'info': 'Payroll reporting.'},

    # March
    {'key': 'gen_fed_tax', 'num': 4, 'quarter': 'Q1', 'scope': 'Federal', 'short': 'Fed Income Tax',
     'title': 'Federal LLC Tax Return (Form 1065 or 1120-S)', 'due_type': 'fixed', 'due_month': 3, 'due_day': 15,
     'due_text': 'March 15', 'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/',
     'info': 'Single-member LLCs report on Schedule C due April 15.'},

    # April
    {'key': 'gen_state_tax', 'num': 5, 'quarter': 'Q2', 'scope': 'State', 'short': 'State LLC Tax',
     'title': 'State Franchise or LLC Minimum Tax', 'due_type': 'fixed', 'due_month': 4, 'due_day': 15,
     'due_text': 'April 15', 'portal_name': 'State Dept of Revenue',
     'portal_url': 'https://www.usa.gov/state-government',
     'info': 'Many states impose a minimum tax or fee to operate.'},
    {'key': 'gen_941_1', 'num': 6, 'quarter': 'Q2', 'scope': 'Federal', 'short': '941 Q1',
     'title': 'Federal Payroll Tax - Q1', 'due_type': 'fixed', 'due_month': 4, 'due_day': 30, 'due_text': 'April 30',
     'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/', 'info': 'Payroll reporting.'},

    # July
    {'key': 'gen_941_2', 'num': 7, 'quarter': 'Q3', 'scope': 'Federal', 'short': '941 Q2',
     'title': 'Federal Payroll Tax - Q2', 'due_type': 'fixed', 'due_month': 7, 'due_day': 31, 'due_text': 'July 31',
     'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/', 'info': 'Payroll reporting.'},

    # October
    {'key': 'gen_941_3', 'num': 8, 'quarter': 'Q4', 'scope': 'Federal', 'short': '941 Q3',
     'title': 'Federal Payroll Tax - Q3', 'due_type': 'fixed', 'due_month': 10, 'due_day': 31, 'due_text': 'October 31',
     'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/', 'info': 'Payroll reporting.'},

    # Rolling / Anniversary Deadlines
    {'key': 'gen_boi', 'num': 9, 'quarter': 'ROLL', 'scope': 'Federal', 'short': 'FinCEN BOI',
     'title': 'Beneficial Ownership Information Report', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
     'due_text': 'Exempt for U.S.-domestic entities (as of 2025)', 'portal_name': 'FinCEN E-Filing',
     'portal_url': 'https://boiefiling.fincen.gov/',
     'info': "Exempt under FinCEN's March 2025 interim final rule — only foreign companies registered to do business in the U.S. must still file. Monitor FinCEN.gov for changes."},
    {'key': 'gen_state_ar', 'num': 10, 'quarter': 'ROLL', 'scope': 'State', 'short': 'State AR',
     'title': 'Secretary of State Annual Report', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
     'due_text': 'Annually', 'portal_name': 'Secretary of State Portal',
     'portal_url': 'https://bizfileonline.sos.ca.gov/',
     'info': 'Maintains LLC good standing. Deadline depends on state of formation.'},
    {'key': 'gen_agent', 'num': 11, 'quarter': 'ROLL', 'scope': 'State', 'short': 'Reg. Agent',
     'title': 'Registered Agent Annual Renewal', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
     'due_text': 'Annually', 'portal_name': 'Agent Portal', 'portal_url': 'https://www.vcorpservices.com/',
     'info': 'Non-payment jeopardizes good standing.'},
    {'key': 'gen_biz_license', 'num': 12, 'quarter': 'ROLL', 'scope': 'Local', 'short': 'Local License',
     'title': 'Municipal / County Business License', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
     'due_text': 'Annually', 'portal_name': 'City Portal', 'portal_url': 'https://www.usa.gov/local-governments',
     'info': 'Required to legally operate a business.'},
    {'key': 'gen_insurance', 'num': 13, 'quarter': 'ROLL', 'scope': 'Insurance', 'short': 'Liability / WC',
     'title': 'General Liability & Workers Comp Insurance', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
     'due_text': 'Annually', 'portal_name': 'Broker', 'portal_url': '#',
     'info': 'Workers Comp is statutorily required if you have employees.'},
    {'key': 'gen_op_agree', 'num': 14, 'quarter': 'ROLL', 'scope': 'Internal', 'short': 'Op Agreement',
     'title': 'LLC Operating Agreement Review', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
     'due_text': 'Annually', 'portal_name': 'Internal', 'portal_url': '#',
     'info': 'Annual member meeting to update resolutions.'}
]

# Generic C-Corp / S-Corp checklist for entities incorporated outside Delaware and
# California, where no state-specific corp template exists. State-specific filings
# still get layered on top via STATE_TASKS_MAP.
GENERAL_CORP_TASKS = [
    # January
    {'key': 'gc_941_4', 'num': 1, 'quarter': 'Q1', 'scope': 'Federal', 'short': '941 Q4',
     'title': 'Employer’s Quarterly Federal Tax Return - Q4', 'due_type': 'fixed', 'due_month': 1, 'due_day': 31,
     'due_text': 'January 31', 'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/', 'info': 'Reconciles federal income tax withholding for Q4.'},
    {'key': 'gc_940', 'num': 2, 'quarter': 'Q1', 'scope': 'Federal', 'short': '940 FUTA',
     'title': 'Federal Annual Unemployment Tax', 'due_type': 'fixed', 'due_month': 1, 'due_day': 31,
     'due_text': 'January 31', 'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/', 'info': 'Assesses FUTA liability on the first $7,000 paid to each W-2 employee.'},
    {'key': 'gc_1099', 'num': 3, 'quarter': 'Q1', 'scope': 'Federal', 'short': '1099-NEC',
     'title': 'Form 1099-NEC Filing & Distribution', 'due_type': 'fixed', 'due_month': 1, 'due_day': 31,
     'due_text': 'January 31', 'portal_name': 'IRS FIRE', 'portal_url': 'https://fire.irs.gov/', 'info': 'Required for unincorporated contractors paid $600+.'},
    {'key': 'gc_w2', 'num': 4, 'quarter': 'Q1', 'scope': 'Federal', 'short': 'W-2 / W-3',
     'title': 'Wage and Tax Statements', 'due_type': 'fixed', 'due_month': 1, 'due_day': 31, 'due_text': 'January 31',
     'portal_name': 'SSA BSO', 'portal_url': 'https://www.ssa.gov/bso/', 'info': 'Transmittal of employee earnings.'},

    # March
    {'key': 'gc_osha', 'num': 5, 'quarter': 'Q1', 'scope': 'Federal', 'short': 'OSHA 300A',
     'title': 'OSHA Form 300A Summary Submission', 'due_type': 'fixed', 'due_month': 3, 'due_day': 2,
     'due_text': 'March 2', 'portal_name': 'OSHA ITA', 'portal_url': 'https://www.osha.gov/injuryreporting/', 'info': 'Electronic submission of work-related injuries/illnesses summary.'},
    {'key': 'gc_aca', 'num': 6, 'quarter': 'Q1', 'scope': 'Federal', 'short': 'ACA 1094/1095-C',
     'title': 'Affordable Care Act Employer Reporting', 'due_type': 'fixed', 'due_month': 3, 'due_day': 31,
     'due_text': 'March 31', 'portal_name': 'IRS AIR', 'portal_url': 'https://www.irs.gov/e-file-providers/air', 'info': 'Electronic filing deadline. Required for Applicable Large Employers (50+ FTEs).'},

    # April
    {'key': 'gc_1120', 'num': 7, 'quarter': 'Q2', 'scope': 'Federal', 'short': 'Form 1120',
     'title': 'U.S. Corporation Income Tax Return', 'due_type': 'fixed', 'due_month': 4, 'due_day': 15,
     'due_text': 'April 15', 'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/', 'info': 'Core federal income tax return. Can be extended to Oct 15 via Form 7004.'},
    {'key': 'gc_1120w_1', 'num': 8, 'quarter': 'Q2', 'scope': 'Federal', 'short': '1120-W Q1',
     'title': 'Fed Est. Tax - Installment 1', 'due_type': 'fixed', 'due_month': 4, 'due_day': 15,
     'due_text': 'April 15', 'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/', 'info': 'Federal estimated tax payment.'},
    {'key': 'gc_state_tax', 'num': 9, 'quarter': 'Q2', 'scope': 'State', 'short': 'State Corp Tax',
     'title': 'State Corporate Income / Franchise Tax Return', 'due_type': 'fixed', 'due_month': 4, 'due_day': 15,
     'due_text': 'April 15', 'portal_name': 'State Dept of Revenue', 'portal_url': 'https://www.usa.gov/state-government', 'info': 'Most states impose a corporate income or franchise tax return separate from the federal 1120.'},
    {'key': 'gc_941_1', 'num': 10, 'quarter': 'Q2', 'scope': 'Federal', 'short': '941 Q1',
     'title': 'Employer’s Quarterly Federal Tax Return - Q1', 'due_type': 'fixed', 'due_month': 4, 'due_day': 30,
     'due_text': 'April 30', 'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/', 'info': 'Reconciles federal income tax withholding for Q1.'},

    # June
    {'key': 'gc_1120w_2', 'num': 11, 'quarter': 'Q2', 'scope': 'Federal', 'short': '1120-W Q2',
     'title': 'Fed Est. Tax - Installment 2', 'due_type': 'fixed', 'due_month': 6, 'due_day': 15, 'due_text': 'June 15',
     'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/', 'info': 'Federal estimated tax payment.'},

    # July
    {'key': 'gc_941_2', 'num': 12, 'quarter': 'Q3', 'scope': 'Federal', 'short': '941 Q2',
     'title': 'Employer’s Quarterly Federal Tax Return - Q2', 'due_type': 'fixed', 'due_month': 7, 'due_day': 31,
     'due_text': 'July 31', 'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/', 'info': 'Reconciles federal income tax withholding for Q2.'},
    {'key': 'gc_5500', 'num': 13, 'quarter': 'Q3', 'scope': 'Federal', 'short': 'Form 5500',
     'title': 'Annual Return/Report of Employee Benefit Plan', 'due_type': 'fixed', 'due_month': 7, 'due_day': 31,
     'due_text': 'July 31', 'portal_name': 'EFAST2', 'portal_url': 'https://www.efast.dol.gov/', 'info': 'Required for 401(k) plans and health/welfare plans with 100+ participants.'},

    # September
    {'key': 'gc_1120w_3', 'num': 14, 'quarter': 'Q3', 'scope': 'Federal', 'short': '1120-W Q3',
     'title': 'Fed Est. Tax - Installment 3', 'due_type': 'fixed', 'due_month': 9, 'due_day': 15,
     'due_text': 'September 15', 'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/', 'info': 'Federal estimated tax payment.'},

    # October
    {'key': 'gc_941_3', 'num': 15, 'quarter': 'Q4', 'scope': 'Federal', 'short': '941 Q3',
     'title': 'Employer’s Quarterly Federal Tax Return - Q3', 'due_type': 'fixed', 'due_month': 10, 'due_day': 31,
     'due_text': 'October 31', 'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/', 'info': 'Reconciles federal income tax withholding for Q3.'},

    # December
    {'key': 'gc_1120w_4', 'num': 16, 'quarter': 'Q4', 'scope': 'Federal', 'short': '1120-W Q4',
     'title': 'Fed Est. Tax - Installment 4', 'due_type': 'fixed', 'due_month': 12, 'due_day': 15,
     'due_text': 'December 15', 'portal_name': 'EFTPS', 'portal_url': 'https://www.eftps.gov/eftps/', 'info': 'Federal estimated tax payment.'},

    # Rolling / Anniversary Deadlines
    {'key': 'gc_boi', 'num': 17, 'quarter': 'ROLL', 'scope': 'Federal', 'short': 'FinCEN BOI',
     'title': 'Beneficial Ownership Information Update', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
     'due_text': 'Exempt for U.S.-domestic entities (as of 2025)', 'portal_name': 'FinCEN E-Filing', 'portal_url': 'https://boiefiling.fincen.gov/',
     'info': "Exempt under FinCEN's March 2025 interim final rule — only foreign companies registered to do business in the U.S. must still file. Monitor FinCEN.gov for changes."},
    {'key': 'gc_state_ar', 'num': 18, 'quarter': 'ROLL', 'scope': 'State', 'short': 'State AR',
     'title': 'Secretary of State Annual Report', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
     'due_text': 'Annually', 'portal_name': 'Secretary of State Portal', 'portal_url': 'https://www.usa.gov/state-government', 'info': 'Maintains corporate good standing. Deadline depends on state of incorporation.'},
    {'key': 'gc_agent', 'num': 19, 'quarter': 'ROLL', 'scope': 'State', 'short': 'Reg. Agent',
     'title': 'Registered Agent Annual Renewal', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
     'due_text': 'Annually', 'portal_name': 'Agent Portal', 'portal_url': 'https://www.vcorpservices.com/', 'info': 'Maintains legal good standing in the state of incorporation.'},
    {'key': 'gc_biz_license', 'num': 20, 'quarter': 'ROLL', 'scope': 'Local', 'short': 'Local License',
     'title': 'Municipal / County Business License', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
     'due_text': 'Annually', 'portal_name': 'City Portal', 'portal_url': 'https://www.usa.gov/local-governments', 'info': 'Required to legally operate a business.'},
    {'key': 'gc_minutes', 'num': 21, 'quarter': 'ROLL', 'scope': 'Internal', 'short': 'Corp Minutes',
     'title': 'Annual Board of Directors & Shareholder Minutes', 'due_type': 'rolling', 'due_month': None,
     'due_day': None, 'due_text': 'Annually', 'portal_name': 'Internal', 'portal_url': '#', 'info': 'Execute Unanimous Written Consents to maintain the corporate veil.'},
    {'key': 'gc_gl', 'num': 22, 'quarter': 'ROLL', 'scope': 'Insurance', 'short': 'Gen. Liab.',
     'title': 'General Liability Insurance Renewal', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
     'due_text': 'Annually', 'portal_name': 'Broker', 'portal_url': '#', 'info': 'Covers physical premise injuries and property damage.'},
    {'key': 'gc_do', 'num': 23, 'quarter': 'ROLL', 'scope': 'Insurance', 'short': 'D&O Insurance',
     'title': 'Directors & Officers Liability Insurance', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
     'due_text': 'Annually', 'portal_name': 'Broker', 'portal_url': '#', 'info': 'Protects board members from personal liability.'},
    {'key': 'gc_wc', 'num': 24, 'quarter': 'ROLL', 'scope': 'Insurance', 'short': 'Workers Comp',
     'title': 'Workers Compensation Insurance Renewal', 'due_type': 'rolling', 'due_month': None, 'due_day': None,
     'due_text': 'Annually', 'portal_name': 'Broker', 'portal_url': '#', 'info': 'Statutory requirement in most states for any W-2 employees.'}
]