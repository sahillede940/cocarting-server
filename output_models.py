from sqlalchemy import Column, BigInteger, String, ForeignKey, TIMESTAMP
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class BlockedUsers(Base):
    __tablename__ = 'blocked_users'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    blocked_user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    block_type = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)

    # Relationships (if needed)
    user = relationship("User", foreign_keys=[user_id])
    blocked_user = relationship("User", foreign_keys=[blocked_user_id])

class Brands(Base):
    __tablename__ = 'brands'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    logo_url = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)

class CategoriesCocarts(Base):
    __tablename__ = 'categories_cocarts'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    cocart_id = Column(BigInteger, nullable=False)
    cocart_category_id = Column(BigInteger, nullable=False)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)

class Charities(Base):
    __tablename__ = 'charities'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    cocart_id = Column(BigInteger, nullable=False)
    user_id = Column(BigInteger, nullable=False)
    first_name = Column(String(255), nullable=False)
    last_name = Column(String(255), nullable=False)
    organization_name = Column(String(255), nullable=False)
    nonprofit_type = Column(String(255), nullable=False)
    ein = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False)
    phone = Column(String(255), nullable=False)
    address = Column(String(255), nullable=False)
    city = Column(String(255), nullable=False)
    zipcode = Column(String(255), nullable=False)
    country = Column(String(255), nullable=False)
    link = Column(String(255), nullable=True)
    vision = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)


class ClippedCoupons(Base):
    __tablename__ = 'clipped_coupons'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    coupon_id = Column(BigInteger, ForeignKey('coupons.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)

    # Unique constraint on user_id and coupon_id
    __table_args__ = (UniqueConstraint('user_id', 'coupon_id', name='clipped_coupons_user_id_coupon_id_unique'),)
    
    # Relationships (if needed)
    user = relationship("User", foreign_keys=[user_id])
    coupon = relationship("Coupon", foreign_keys=[coupon_id])

class CocartCategories(Base):
    __tablename__ = 'cocart_categories'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    display_name = Column(String(255), nullable=False)
    logo_url = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)

class CocartLikes(Base):
    __tablename__ = 'cocart_likes'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    cocart_id = Column(BigInteger, ForeignKey('cocarts.id', ondelete='CASCADE'), nullable=False)
    deleted_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)

    # Relationships (if needed)
    user = relationship("User", foreign_keys=[user_id])
    cocart = relationship("Cocart", foreign_keys=[cocart_id])


class CocartMessages(Base):
    __tablename__ = 'cocart_messages'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    message = Column(String, nullable=False)
    image_url = Column(String(255), nullable=True)
    attachement = Column(String(255), nullable=True)
    attachment_type = Column(Integer, nullable=True)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    cocart_id = Column(BigInteger, ForeignKey('cocarts.id', ondelete='CASCADE'), nullable=False)
    read_at = Column(TIMESTAMP, nullable=True)
    deleted_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)
    product_id = Column(BigInteger, ForeignKey('products.id', ondelete='CASCADE'), nullable=True)
    product_url = Column(String(255), nullable=True)

    # Relationships (if needed)
    user = relationship("User", foreign_keys=[user_id])
    cocart = relationship("Cocart", foreign_keys=[cocart_id])
    product = relationship("Product", foreign_keys=[product_id])


class CocartProductDownvotes(Base):
    __tablename__ = 'cocart_product_downvotes'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    cocart_id = Column(BigInteger, ForeignKey('cocarts.id', ondelete='CASCADE'), nullable=True)
    cocart_product_id = Column(BigInteger, ForeignKey('cocart_products.id', ondelete='CASCADE'), nullable=True)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    product_id = Column(BigInteger, ForeignKey('products.id', ondelete='CASCADE'), nullable=True)
    deleted_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)

    # Relationships (if needed)
    cocart = relationship("Cocart", foreign_keys=[cocart_id])
    cocart_product = relationship("CocartProduct", foreign_keys=[cocart_product_id])
    user = relationship("User", foreign_keys=[user_id])
    product = relationship("Product", foreign_keys=[product_id])


class CocartProductUpvotes(Base):
    __tablename__ = 'cocart_product_upvotes'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    cocart_id = Column(BigInteger, ForeignKey('cocarts.id', ondelete='CASCADE'), nullable=True)
    cocart_product_id = Column(BigInteger, ForeignKey('cocart_products.id', ondelete='CASCADE'), nullable=True)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    product_id = Column(BigInteger, ForeignKey('products.id', ondelete='CASCADE'), nullable=True)
    deleted_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)

    # Relationships (if needed)
    cocart = relationship("Cocart", foreign_keys=[cocart_id])
    cocart_product = relationship("CocartProduct", foreign_keys=[cocart_product_id])
    user = relationship("User", foreign_keys=[user_id])
    product = relationship("Product", foreign_keys=[product_id])


class CocartProducts(Base):
    __tablename__ = 'cocart_products'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    cocart_id = Column(BigInteger, ForeignKey('cocarts.id', ondelete='CASCADE'), nullable=True)
    product_id = Column(BigInteger, ForeignKey('products.id', ondelete='CASCADE'), nullable=True)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    deleted_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)
    is_bought = Column(Integer, nullable=False, default=0)
    is_claimed = Column(Integer, nullable=False, default=0)

    # Relationships (if needed)
    cocart = relationship("Cocart", foreign_keys=[cocart_id])
    product = relationship("Product", foreign_keys=[product_id])
    user = relationship("User", foreign_keys=[user_id])


class CocartShares(Base):
    __tablename__ = 'cocart_shares'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    cocart_id = Column(BigInteger, ForeignKey('cocarts.id', ondelete='CASCADE'), nullable=False)
    type = Column(Integer, nullable=False, default=0)
    deleted_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)

    # Relationships (if needed)
    user = relationship("User", foreign_keys=[user_id])
    cocart = relationship("Cocart", foreign_keys=[cocart_id])


class CocartUsers(Base):
    __tablename__ = 'cocart_users'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    cocart_id = Column(BigInteger, ForeignKey('cocarts.id', ondelete='CASCADE'), nullable=False)
    deleted_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)
    is_read = Column(Integer, default=0)

    # Relationships (if needed)
    user = relationship("User", foreign_keys=[user_id])
    cocart = relationship("Cocart", foreign_keys=[cocart_id])


class Cocarts(Base):
    __tablename__ = 'cocarts'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    type = Column(Integer, nullable=False, default=0)
    name = Column(String(255), nullable=False)
    description = Column(String, nullable=True)
    slug = Column(String(255), nullable=False, unique=True)
    deleted_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)
    thumbnail = Column(String(255), nullable=True)
    allow_vote = Column(Integer, nullable=False, default=0)
    allow_add_product = Column(Integer, nullable=False, default=0)
    allow_remove_product = Column(Integer, nullable=False, default=0)
    mark_purchased_items = Column(Integer, nullable=False, default=0)
    is_read = Column(Integer, nullable=False, default=0)
    is_hide = Column(Integer, nullable=False, default=0)

    # Relationships (if needed)
    user = relationship("User", foreign_keys=[user_id])


class Compare(Base):
    __tablename__ = 'compare'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    product_id = Column(BigInteger, ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    product_source = Column(BigInteger, nullable=False)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)

    # Relationships (if needed)
    user = relationship("User", foreign_keys=[user_id])
    product = relationship("Product", foreign_keys=[product_id])

class ContactForms(Base):
    __tablename__ = 'contact_forms'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True)
    choice = Column(String(255), nullable=True)
    subject = Column(String(255), nullable=True)
    message = Column(String, nullable=True)
    deleted_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)
    name = Column(String(255), nullable=True)
    phone = Column(String(255), nullable=True)

    # Relationships (if needed)
    user = relationship("User", foreign_keys=[user_id])




class Contacts(Base):
    __tablename__ = 'contacts'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    user_contact_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    deleted_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)

    # Relationships (if needed)
    user = relationship("User", foreign_keys=[user_id])
    contact_user = relationship("User", foreign_keys=[user_contact_id])


class Coupon(Base):
    __tablename__ = 'coupon'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    features = Column(String(255), nullable=True)
    brand = Column(String(255), nullable=True)
    brand_id = Column(BigInteger, ForeignKey('brands.id', ondelete='CASCADE'), nullable=True)
    coupon_code = Column(String(255), nullable=True)
    description = Column(String, nullable=True)
    categories = Column(String(255), nullable=True)
    regions = Column(String(255), nullable=True)
    deeplink_tracking = Column(String(255), nullable=True)
    logo = Column(String(255), nullable=True)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    deleted_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)

    # Relationships (if needed)
    brand_relation = relationship("Brands", foreign_keys=[brand_id])


class CouponRedeems(Base):
    __tablename__ = 'coupon_redeems'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    coupon_id = Column(BigInteger, ForeignKey('coupons.id', ondelete='CASCADE'), nullable=True)
    cocart_id = Column(BigInteger, ForeignKey('cocarts.id', ondelete='CASCADE'), nullable=True)
    deleted_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)

    # Relationships (if needed)
    user = relationship("User", foreign_keys=[user_id])
    coupon = relationship("Coupon", foreign_keys=[coupon_id])
    cocart = relationship("Cocart", foreign_keys=[cocart_id])


class FailedJobs(Base):
    __tablename__ = 'failed_jobs'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    uuid = Column(String(255), unique=True, nullable=False)
    connection = Column(String, nullable=False)
    queue = Column(String, nullable=False)
    payload = Column(String, nullable=False)
    exception = Column(String, nullable=False)
    failed_at = Column(TIMESTAMP, nullable=False, default=datetime.utcnow)


from sqlalchemy.dialects.mysql import JSON

class FaqSections(Base):
    __tablename__ = 'faq_sections'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    question = Column(String(255), nullable=False)
    answer = Column(JSON, nullable=False)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)


class Friends(Base):
    __tablename__ = 'friends'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    friend_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    is_following = Column(Integer, nullable=False, default=1)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)

    # Relationships (if needed)
    user = relationship("User", foreign_keys=[user_id])
    friend = relationship("User", foreign_keys=[friend_id])


class Giftcards(Base):
    __tablename__ = 'giftcards'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    loyalty_task_id = Column(BigInteger, ForeignKey('loyalty_tasks.id', ondelete='CASCADE'), nullable=False)
    logo_url = Column(String(255), nullable=False)
    reward_title = Column(String(255), nullable=False)
    redeem_url = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)

    # Relationships (if needed)
    loyalty_task = relationship("LoyaltyTasks", foreign_keys=[loyalty_task_id])




class HelpSections(Base):
    __tablename__ = 'help_sections'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(String, nullable=True)
    action_label = Column(String(255), nullable=True)
    items = Column(JSON, nullable=True)
    expanded = Column(Integer, nullable=False, default=0)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)


class HiddenPosts(Base):
    __tablename__ = 'hidden_posts'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    post_id = Column(BigInteger, ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)

    # Relationships (if needed)
    user = relationship("User", foreign_keys=[user_id])
    post = relationship("Post", foreign_keys=[post_id])


class Jobs(Base):
    __tablename__ = 'jobs'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    queue = Column(String(255), nullable=False)
    payload = Column(String, nullable=False)
    attempts = Column(Integer, nullable=False)
    reserved_at = Column(Integer, nullable=True)
    available_at = Column(Integer, nullable=False)
    created_at = Column(Integer, nullable=False)

    # Index for queue column
    __table_args__ = (Index('jobs_queue_index', 'queue'),)


class LoyaltyTasks(Base):
    __tablename__ = 'loyalty_tasks'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    loyalty_name = Column(String(255), nullable=True)
    number_of_wishlist = Column(Integer, default=0)
    add_product_to_any_wishlist = Column(Integer, default=0)
    new_user_sign_up = Column(Integer, default=0)
    invite_people_private_wishlist = Column(Integer, default=0)
    add_product_externally_to_wishlist = Column(Integer, default=0)
    click_through_to_buy_a_product = Column(Integer, default=0)
    send_chat_message_in_any_wishlist = Column(Integer, default=0)
    add_multiple_products_to_each_wishList = Column(Integer, default=0)
    click_through_to_buy_a_product_on_different_days = Column(Integer, default=0)
    invite_people_to_wishlist = Column(Integer, default=0)
    create_cocarting_post = Column(Integer, default=0)
    like_cocarting_on_facebook = Column(Integer, default=0)
    add_cocarting_app_review_on_store = Column(Integer, default=0)
    invite_people_to_your_wishlists = Column(Integer, default=0)
    use_compare_items_feature = Column(Integer, default=0)
    create_cocarting_poll = Column(Integer, default=0)
    like_cocarting_on_instagram = Column(Integer, default=0)
    visit_coupon_details_page = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)


class Migrations(Base):
    __tablename__ = 'migrations'

    id = Column(Integer, primary_key=True, autoincrement=True)
    migration = Column(String(255), nullable=False)
    batch = Column(Integer, nullable=False)


class Newsletter(Base):
    __tablename__ = 'newsletter'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)


class Newsletters(Base):
    __tablename__ = 'newsletters'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    email = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)


class NotificationPreferences(Base):
    __tablename__ = 'notification_preferences'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    category = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    email = Column(Integer, nullable=False, default=0)
    sms = Column(Integer, nullable=False, default=0)
    push = Column(Integer, nullable=False, default=0)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)

    # Relationships (if needed)
    user = relationship("User", foreign_keys=[user_id])



class Notifications(Base):
    __tablename__ = 'notifications'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    cocart_id = Column(BigInteger, ForeignKey('cocarts.id', ondelete='CASCADE'), nullable=True)
    product_id = Column(BigInteger, ForeignKey('products.id', ondelete='CASCADE'), nullable=True)
    user_notification_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    title = Column(String(255), nullable=True)
    notification = Column(String(255), nullable=True)
    type = Column(String(255), nullable=True)
    url = Column(String(255), nullable=True)
    read_at = Column(TIMESTAMP, nullable=True)
    deleted_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)
    extra_data = Column(String, nullable=True)
    is_joined = Column(Integer, nullable=True)

    # Relationships (if needed)
    user = relationship("User", foreign_keys=[user_id])
    cocart = relationship("Cocart", foreign_keys=[cocart_id])
    product = relationship("Product", foreign_keys=[product_id])
    user_notification = relationship("User", foreign_keys=[user_notification_id])



class Organizations(Base):
    __tablename__ = 'organizations'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    country = Column(String(255), nullable=True)
    zip_code = Column(String(255), nullable=True)
    address_one = Column(String(255), nullable=True)
    address_two = Column(String(255), nullable=True)
    city = Column(String(255), nullable=True)
    state = Column(String(255), nullable=True)
    phone = Column(String(255), nullable=True)
    website_url = Column(String(255), nullable=True)
    latitude = Column(String(255), nullable=True)
    longitude = Column(String(255), nullable=True)
    organization_type = Column(String(255), nullable=True)
    product_types = Column(String(255), nullable=True)
    referrer = Column(String(255), nullable=True)
    number_of_donations = Column(String(255), nullable=True)
    deleted_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)

    # Relationships (if needed)
    user = relationship("User", foreign_keys=[user_id])


class PasswordResetTokens(Base):
    __tablename__ = 'password_reset_tokens'

    email = Column(String(255), primary_key=True, nullable=False)
    token = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, nullable=True)


class PasswordResets(Base):
    __tablename__ = 'password_resets'

    email = Column(String(255), primary_key=True, nullable=False)
    token = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, nullable=True)

    # Index for email column
    __table_args__ = (Index('password_resets_email_index', 'email'),)



class PersonalAccessTokens(Base):
    __tablename__ = 'personal_access_tokens'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    tokenable_type = Column(String(255), nullable=False)
    tokenable_id = Column(BigInteger, nullable=False)
    name = Column(String(255), nullable=False)
    token = Column(String(64), nullable=False, unique=True)
    abilities = Column(String, nullable=True)
    last_used_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)
    expires_at = Column(TIMESTAMP, nullable=True)

    # Index for combined columns tokenable_type and tokenable_id
    __table_args__ = (Index('personal_access_tokens_tokenable_type_tokenable_id_index', 'tokenable_type', 'tokenable_id'),)


class PollOptions(Base):
    __tablename__ = 'poll_options'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    poll_id = Column(BigInteger, ForeignKey('polls.id', ondelete='CASCADE'), nullable=False)
    option_text = Column(String(255), nullable=False)
    description = Column(String(255), nullable=True)
    option_url = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)

    # Relationships (if needed)
    poll = relationship("Poll", foreign_keys=[poll_id])


class PollVotes(Base):
    __tablename__ = 'poll_votes'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    poll_option_id = Column(BigInteger, ForeignKey('poll_options.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)

    # Relationships (if needed)
    poll_option = relationship("PollOptions", foreign_keys=[poll_option_id])
    user = relationship("User", foreign_keys=[user_id])


class Polls(Base):
    __tablename__ = 'polls'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    pollable_id = Column(BigInteger, nullable=False)
    pollable_type = Column(String(255), nullable=False)
    question = Column(String(255), nullable=False)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)

    # Relationships (if needed)
    user = relationship("User", foreign_keys=[user_id])


class PostComments(Base):
    __tablename__ = 'post_comments'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    post_id = Column(BigInteger, ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)
    comment = Column(String, nullable=False)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)

    # Relationships (if needed)
    user = relationship("User", foreign_keys=[user_id])
    post = relationship("Post", foreign_keys=[post_id])


class PostLikes(Base):
    __tablename__ = 'post_likes'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    post_id = Column(BigInteger, ForeignKey('posts.id', ondelete='CASCADE'), nullable=False)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)

    # Relationships (if needed)
    user = relationship("User", foreign_keys=[user_id])
    post = relationship("Post", foreign_keys=[post_id])


class Posts(Base):
    __tablename__ = 'posts'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    content = Column(String, nullable=False)
    post_image = Column(String(255), nullable=True)
    reposted_post_id = Column(BigInteger, ForeignKey('posts.id', ondelete='CASCADE'), nullable=True)
    shares = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)
    type = Column(Integer, default=1)

    # Relationships (if needed)
    user = relationship("User", foreign_keys=[user_id])
    reposted_post = relationship("Posts", remote_side=[id])


class ProductAttributes(Base):
    __tablename__ = 'product_attributes'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    cocart_id = Column(BigInteger, ForeignKey('cocarts.id', ondelete='CASCADE'), nullable=True)
    title = Column(String(255), nullable=True)
    attribute = Column(String(255), nullable=True)
    deleted_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)

    # Relationships (if needed)
    cocart = relationship("Cocarts", foreign_keys=[cocart_id])


class ProductCategories(Base):
    __tablename__ = 'product_categories'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    category = Column(String(255), nullable=True)
    slug = Column(String(255), nullable=False, unique=True)
    deleted_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)
    product_category_id = Column(BigInteger, ForeignKey('product_categories.id', ondelete='CASCADE'), nullable=True)

    # Self-referential relationship (if needed)
    parent_category = relationship("ProductCategories", remote_side=[id])


class ProductFavorites(Base):
    __tablename__ = 'product_favorites'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    product_id = Column(BigInteger, ForeignKey('products.id', ondelete='CASCADE'), nullable=True)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    cocart_id = Column(BigInteger, ForeignKey('cocarts.id', ondelete='CASCADE'), nullable=True)
    deleted_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)

    # Relationships (if needed)
    product = relationship("Product", foreign_keys=[product_id])
    user = relationship("User", foreign_keys=[user_id])
    cocart = relationship("Cocart", foreign_keys=[cocart_id])


class ProductImages(Base):
    __tablename__ = 'product_images'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    product_id = Column(BigInteger, ForeignKey('products.id', ondelete='CASCADE'), nullable=True)
    image = Column(String, nullable=True)
    thumbnail = Column(String(255), nullable=True)
    medium_image = Column(String(255), nullable=True)
    large_image = Column(String(255), nullable=True)
    deleted_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)

    # Relationships (if needed)
    product = relationship("Product", foreign_keys=[product_id])


class ProductReviews(Base):
    __tablename__ = 'product_reviews'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    product_id = Column(BigInteger, ForeignKey('products.id', ondelete='CASCADE'), nullable=False)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    rating = Column(String(255), nullable=True)
    review = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)
    deleted_at = Column(TIMESTAMP, nullable=True)

    # Relationships (if needed)
    product = relationship("Product", foreign_keys=[product_id])
    user = relationship("User", foreign_keys=[user_id])


class Products(Base):
    __tablename__ = 'products'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    product_category_id = Column(BigInteger, ForeignKey('product_categories.id', ondelete='CASCADE'), nullable=True)
    name = Column(String(255), nullable=False)
    short_description = Column(String, nullable=True)
    description = Column(String, nullable=True)
    brand_name = Column(String(255), nullable=True)
    product_tracking_url = Column(String(2500), nullable=True)
    standard_shipping_rate = Column(String(255), nullable=True)
    size = Column(String(255), nullable=True)
    color = Column(String(255), nullable=True)
    marketplace = Column(Integer, nullable=False, default=0)
    model_number = Column(String(255), nullable=True)
    seller_info = Column(String(255), nullable=True)
    customer_rating = Column(String(255), nullable=True)
    number_of_reviews = Column(Integer, nullable=True)
    rhid = Column(String(255), nullable=True)
    bundle = Column(Integer, nullable=False, default=1)
    clearance = Column(Integer, nullable=False, default=1)
    preorder = Column(Integer, nullable=False, default=1)
    stock = Column(String(255), nullable=True)
    freight = Column(Integer, nullable=False, default=1)
    gender = Column(String(255), nullable=True, default='m')
    affiliate_add_to_cart_url = Column(String(2500), nullable=True)
    max_number_of_qty = Column(Integer, nullable=True)
    offer_type = Column(Integer, nullable=True)
    available_online = Column(Integer, nullable=False, default=0)
    e_delivery = Column(Integer, nullable=False, default=1)
    deleted_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)
    product_image_id = Column(BigInteger, ForeignKey('product_images.id', ondelete='CASCADE'), nullable=True)
    price = Column(Float, nullable=True)
    original_price = Column(Float, nullable=True)
    slug = Column(String(255), nullable=False, unique=True)
    wm_product_id = Column(String(255), nullable=True)
    product_source = Column(Integer, nullable=False, default=0)
    amazon_id = Column(String(255), nullable=True)
    added_by = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=True)

    # Relationships (if needed)
    category = relationship("ProductCategories", foreign_keys=[product_category_id])
    image = relationship("ProductImages", foreign_keys=[product_image_id])
    added_by_user = relationship("User", foreign_keys=[added_by])


class Reports(Base):
    __tablename__ = 'reports'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    reported_user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    reported_post_id = Column(BigInteger, ForeignKey('posts.id', ondelete='CASCADE'), nullable=True)
    report_type = Column(Enum('Post', 'Member'), nullable=False)
    report_reason = Column(String, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)
    deleted_at = Column(TIMESTAMP, nullable=True)

    # Relationships (if needed)
    user = relationship("User", foreign_keys=[user_id])
    reported_user = relationship("User", foreign_keys=[reported_user_id])
    reported_post = relationship("Posts", foreign_keys=[reported_post_id])


class Retailers(Base):
    __tablename__ = 'retailers'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, unique=True)
    logo_url = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)


from sqlalchemy.dialects.mysql import JSON

class SaveSharingProducts(Base):
    __tablename__ = 'save_sharing_products'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    platform = Column(String(255), nullable=False)
    title = Column(String(255), nullable=False)
    sections = Column(JSON, nullable=False)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)


class SocialAccounts(Base):
    __tablename__ = 'social_accounts'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    provider_name = Column(String(255), nullable=False)
    provider_id = Column(String(255), nullable=False)
    
    # Relationships (if needed)
    user = relationship("User", foreign_keys=[user_id])


class Tasks(Base):
    __tablename__ = 'tasks'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    description = Column(String, nullable=False)
    type = Column(Enum('Ruby', 'Sapphire', 'Diamond'), nullable=False)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)
    quantity = Column(Integer, nullable=False, default=1)


from sqlalchemy.dialects.mysql import JSON

class TipsAndTricks(Base):
    __tablename__ = 'tips_and_tricks'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    title = Column(String(255), nullable=False)
    content = Column(JSON, nullable=False)
    expanded = Column(Integer, nullable=False, default=0)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)


class UserFavoriteBrandsRetailers(Base):
    __tablename__ = 'user_favorite_brands_retailers'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    brand_id = Column(BigInteger, ForeignKey('brands.id', ondelete='CASCADE'), nullable=True)
    retailer_id = Column(BigInteger, ForeignKey('retailers.id', ondelete='CASCADE'), nullable=True)
    favorite_type = Column(String(255), nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)

    # Relationships (if needed)
    user = relationship("User", foreign_keys=[user_id])
    brand = relationship("Brands", foreign_keys=[brand_id])
    retailer = relationship("Retailers", foreign_keys=[retailer_id])


class UserInvites(Base):
    __tablename__ = 'user_invites'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    cocart_id = Column(BigInteger, ForeignKey('cocarts.id', ondelete='CASCADE'), nullable=True)
    email = Column(String(255), nullable=True)
    phone = Column(String(255), nullable=True)
    deleted_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)
    hash = Column(String(255), nullable=False, unique=True)
    invitee_id = Column(Integer, nullable=True)

    # Relationships (if needed)
    user = relationship("User", foreign_keys=[user_id])
    cocart = relationship("Cocart", foreign_keys=[cocart_id])


class UserLoyalty(Base):
    __tablename__ = 'user_loyalty'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    loyalty_id = Column(BigInteger, ForeignKey('loyalty_tasks.id', ondelete='CASCADE'), nullable=True)
    user_id = Column(BigInteger, ForeignKey('users.id', ondelete='CASCADE'), nullable=True)
    number_of_wishlist = Column(Integer, default=0)
    add_product_to_any_wishlist = Column(Integer, default=0)
    new_user_sign_up = Column(Integer, default=0)
    invite_people_private_wishlist = Column(Integer, default=0)
    add_product_externally_to_wishlist = Column(Integer, default=0)
    click_through_to_buy_a_product = Column(Integer, default=0)
    send_chat_message_in_any_wishlist = Column(Integer, default=0)
    add_multiple_products_to_each_wishList = Column(Integer, default=0)
    click_through_to_buy_a_product_on_different_days = Column(Integer, default=0)
    invite_people_to_wishlist = Column(Integer, default=0)
    create_cocarting_post = Column(Integer, default=0)
    like_cocarting_on_facebook = Column(Integer, default=0)
    add_cocarting_app_review_on_store = Column(Integer, default=0)
    invite_people_to_your_wishlists = Column(Integer, default=0)
    use_compare_items_feature = Column(Integer, default=0)
    create_cocarting_poll = Column(Integer, default=0)
    like_cocarting_on_instagram = Column(Integer, default=0)
    visit_coupon_details_page = Column(Integer, default=0)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)

    # Relationships (if needed)
    loyalty_task = relationship("LoyaltyTasks", foreign_keys=[loyalty_id])
    user = relationship("User", foreign_keys=[user_id])


class Users(Base):
    __tablename__ = 'users'

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=True)
    first_name = Column(String(255), nullable=True)
    last_name = Column(String(255), nullable=True)
    email = Column(String(255), nullable=True, unique=True)
    phone = Column(String(255), nullable=True)
    login_type = Column(Integer, nullable=False, default=0)
    account_type = Column(Integer, nullable=True)
    facebook_id = Column(String(255), nullable=True)
    google_id = Column(String(255), nullable=True)
    apple_id = Column(String(255), nullable=True)
    verified = Column(Integer, nullable=False, default=1)
    token = Column(String(255), nullable=True)
    verify_token = Column(String(255), nullable=True)
    verify_token_until = Column(TIMESTAMP, nullable=True)
    device = Column(Integer, nullable=False, default=0)
    email_verified_at = Column(TIMESTAMP, nullable=True)
    password = Column(String(255), nullable=False)
    remember_token = Column(String(100), nullable=True)
    deleted_at = Column(TIMESTAMP, nullable=True)
    created_at = Column(TIMESTAMP, nullable=True)
    updated_at = Column(TIMESTAMP, nullable=True)
    latitude = Column(String(255), nullable=True)
    longitude = Column(String(255), nullable=True)
    username = Column(String(255), nullable=False, unique=True)
    address_one = Column(String(255), nullable=True)
    address_two = Column(String(255), nullable=True)
    city = Column(String(255), nullable=True)
    state = Column(String(255), nullable=True)
    zip_code = Column(String(255), nullable=True)
    gender = Column(String(255), nullable=True)
    country = Column(String(255), nullable=True)
    apt = Column(String(255), nullable=True)
    phone_number = Column(String(255), nullable=True, unique=True)
    avatar = Column(String(1024), nullable=True)
    selected_cocart_id = Column(BigInteger, ForeignKey('cocarts.id', ondelete='CASCADE'), nullable=True)
    phone_verification_code = Column(String(255), nullable=True)
    phone_verification_code_expire_at = Column(TIMESTAMP, nullable=True)
    phone_is_verified = Column(Integer, nullable=False, default=0)
    onesignal_subscription_ids = Column(String, nullable=True)
    onesignal_subscription_id = Column(String, nullable=True)
    account_verified = Column(Integer, nullable=True, default=0)

    # Relationships (if needed)
    selected_cocart = relationship("Cocarts", foreign_keys=[selected_cocart_id])
