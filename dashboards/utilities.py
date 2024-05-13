from entities.models import GlobalCompanies, generate_random_gc_id, in_global_companies
from entities.utilities import currency_to_country

def extract_domain_from_email(email):
    """Creates a domain name from the email provided"""
    if '@' not in email:
        return "Invalid email format"  # Early return if email does not contain '@'

    try:
        # Extract the domain part after '@'
        domain_part = email.split('@')[1]
        # Clean up the domain to remove any paths or parameters that could erroneously be included
        domain = domain_part.split('/')[0]  # Just in case the email contains a path (rare but could happen in malformed strings)
        return domain
    except IndexError:
        return "Invalid email format"


def get_customer_info(customer_name, url, txn): 
    """Extracts information from the entity provided. If no company exists then a company is created."""
    attempts = 2 

    while attempts > 0:
        try:
            # Fetch the customer from the DashboardData model using provided name and URL
            customer = GlobalCompanies.objects.get(name=customer_name, url=url)
            # Prepare a dictionary with the required details
            customer_details = {
                'city': customer.city,
                'state': customer.state,
                'country': customer.country,
                'size': customer.size,
                'sector': customer.sector,
                'p_and_l_category': customer.p_and_l_category,
                'p_and_l_subcategory': customer.p_and_l_subcategory,
            }
            return customer_details
        except GlobalCompanies.DoesNotExist:
            create_global_company(txn)
        except Exception as e:
            # Optional: handle unexpected errors
            return f"An error occurred: {str(e)}"

        attempts -= 1


def create_global_company(txn):
    """Creates a globalCompany entity if none exists"""
    # Initialize default values
    email = "unknown@unknown.com" 
    currency = "Unknown"
    name = "Unknown"
    city = "Unknown"
    state = "Unknown"

    # Safely extract email
    bill_email = txn.get('BillEmail', {})
    if isinstance(bill_email, dict):
        email = bill_email.get('Address', email)

    # Safely extract currency name
    currency_ref = txn.get('CurrencyRef', {})
    if isinstance(currency_ref, dict):
        currency = currency_ref.get('name', currency)

    # Safely extract shipping or remittance address
    ship_addr = txn.get('ShipAddr', txn.get('RemitToAddr', {}))
    if isinstance(ship_addr, dict):
        city = ship_addr.get('City', city)
        state = ship_addr.get('CountrySubDivisionCode', state)

    # Safely extract customer or entity name
    customer_ref = txn.get('CustomerRef', txn.get('EntityRef', {}))
    if isinstance(customer_ref, dict):
        name = customer_ref.get('name', name)

    new_company = GlobalCompanies.objects.create(
        gc_id = generate_random_gc_id(),
        name = name,
        url = extract_domain_from_email(email),
        image = None,
        city = city,
        state = state,
        country = currency_to_country(currency),
        size = "Unknown",
        sector = "Unknown",
    )
    # # Properly manage many-to-many relationship
    # FIX THIS!
    # new_company.mm_Companies.add([request.user.id])

    print("Company", name, "added to Global Companies")


