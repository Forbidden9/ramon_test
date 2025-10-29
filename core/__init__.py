from fastapi import APIRouter
from core.oauth.router import oauth2
from core.user.router import user
from core.tag.router import tag
from core.post.router import post
from core.comment.router import comment


router = APIRouter()

router.include_router(oauth2, tags=["oauth2"], prefix="/api/oauth2")
router.include_router(user, tags=["user"], prefix="/api/user")
router.include_router(tag, tags=["tag"], prefix="/api/tag")
router.include_router(post, tags=["post"], prefix="/api/post")
router.include_router(comment, tags=["comment"], prefix="/api/comment")